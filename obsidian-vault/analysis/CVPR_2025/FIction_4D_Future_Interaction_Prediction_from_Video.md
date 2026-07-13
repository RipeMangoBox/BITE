---
title: FIction 4D Future Interaction Prediction from Video
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/FIction_4D_Future_Interaction_Prediction_from_Video.pdf
project_link: null
code_link: null
aliases:
- F4FIPFV
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 显式地将3D场景体素化表示与视频、人体姿态等多模态信息融合，并通过CVAE对每个交互位置生成姿态分布。
primary_logic: 人类的活动意图与环境中的物体布局紧密耦合，因此必须利用3D环境上下文来同时预测未来交互的“在哪里”和“如何”交互。
claims:
- 方法在Cooking、Bike Repair、Health三个场景的交互位置预测和姿态预测上均显著优于现有最佳方法，相对增益超过30%。
- 去除3D环境上下文导致位置预测性能急剧下降（例如Cooking场景PR从21.0降至9.9），证实环境建模的关键性。
- 在姿态预测中，相比最佳基线MPJPE降低高达49mm（Health场景）。
- Cooking 上 PR-AUC = 21.0 (FICTION)
---

# FIction 4D Future Interaction Prediction from Video

> [!tip] 核心洞察
> 人类的活动意图与环境中的物体布局紧密耦合，因此必须利用3D环境上下文来同时预测未来交互的“在哪里”和“如何”交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | FICTION：从视频进行4D未来交互预测 |
| 英文题名 | FIction 4D Future Interaction Prediction from Video |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FICTION |
| Dataset | Cooking, Health |

> [!tip] 效果简介
> - Cooking 上，PR-AUC 21.0 (FICTION) vs 16.9 (OCT ) (+4.1 (24.3%))；Chamfer Distance 7.4 (FICTION) vs 9.0 (OCT ) (-1.6)；MPJPE 229 (FICTION) vs 264 (T2M-GPT-FT) (-35 (13.3%))。
> - Health 上，MPJPE 172 (FICTION) vs 221 (T2M-GPT-FT) (-49 (22.2%))。

## 概要

预测人类未来的行为——尤其是“将在哪里与何物交互”以及“将以何种姿态交互”——是构建具身智能助手的关键能力。现有方法大多将交互预测局限于二维图像空间，例如预测下一帧的动作热图或自回归地生成动作标签，忽略了持久性的三维场景上下文和物体布局。这种信息缺失导致模型难以准确预测长时间跨度、多物体交互的位置和姿态。

FICTION 方法的核心洞察在于：人类的活动意图与所处环境中的物体布局紧密耦合。因此，要同时回答“在哪里交互”和“如何交互”这两个问题，必须显式地利用三维环境上下文。基于这一思想，FICTION 将过去观察到的视频、人体姿态序列与三维场景体素表示（包含物体布局和演员位置）进行多模态融合，通过一个多模态 Transformer 编码器生成统一的上下文表示。在此基础上，模型分别预测未来交互的三维位置（以二元体素网格形式）和每个交互位置处的姿态分布（通过条件变分自编码器 CVAE 生成）。

在 Ego-Exo4D 数据集上，FICTION 在烹饪、自行车修理和健康三个场景的交互位置预测和姿态预测任务上均显著优于现有最佳方法，相对增益超过 30%。具体而言，在烹饪场景的位置预测中，FICTION 的 PR-AUC 达到 21.0，相比最佳基线 OCT 的 16.9 提升了 24.3%；在姿态预测中，相比最佳基线 T2M-GPT-FT，MPJPE 在烹饪场景降低 35mm（13.3%），在健康场景降低 49mm（22.2%）。消融实验进一步证实，移除三维环境上下文会导致位置预测性能急剧下降（烹饪场景 PR-AUC 从 21.0 降至 9.9），从而验证了环境建模在任务中的关键作用。

人类在日常活动中持续与周围物体发生交互——制作奶茶时需要接触饮水机、炉灶、杯具，修理自行车时则需操作轮胎、扳手等工具。这种交互行为在空间上具有高度结构化特征：**交互发生的位置**（“在哪里”）与**交互时的身体姿态**（“如何交互”）紧密耦合于三维环境的物体布局。例如，取水时双手配合水龙头的高度，取高处橱柜物品时身体需伸展，这些姿态选择无法脱离场景上下文而被独立预测。

然而，现有方法将交互预测问题局限于二维空间。代表性工作如**HierVL**采用自回归方式在2D视频帧上预测未来动作标签，**OCT**则通过2D热图预测交互热点再将其提升至3D空间。这些方法的核心瓶颈在于：**忽略持久性的3D场景上下文和物体布局**，导致无法准确预测长时间、多物体交互的位置与姿态。当活动涉及多个分散的交互目标且观察时间跨度较长时，缺乏环境约束的模型难以区分“人将走向冰箱”还是“走向橱柜”，更无法生成与物体高度、形状相匹配的合理人体姿态。

上述瓶颈催生了本文的核心动机：**人类的活动意图与环境中的物体布局紧密耦合，因此必须显式利用3D环境上下文来同时预测未来交互的“在哪里”和“如何”交互**。这要求模型不仅理解“人正在做什么”（从视频中捕捉），还需理解“环境中有什么、在哪里”（从3D场景表示中获取），并将两者融合以推断未来的交互时空分布。

基于此，本文提出**FICTION**（**F**uture **I**nteraction Predi**cti**on from Vide**o** and 3D Scen**e** Co**n**text），将任务形式化为两个子问题：给定观察视频 $\mathcal{V}_{0:\tau_o}$ 和3D场景点云 $\mathcal{P}$，（1）预测所有未来交互发生的3D位置集合 $\mathcal{F}_o(\mathcal{V}_{0:\tau_o}, \mathcal{P})$；（2）对任意查询位置 $\mathbf{x}_{\tau_k}$，输出该处交互姿态的分布 $\mathcal{F}_p(\mathcal{V}_{0:\tau_o}, \mathcal{P}, \mathbf{x}_{\tau_k}) = \mathbb{P}(\theta, t)$，其中 $\theta$ 为SMPL姿态参数，$t$ 为全局位置。这一形式化首次将“位置预测”与“姿态预测”统一于3D环境条件下，填补了从2D视频理解到4D（3D空间+时间）交互预测的范式缺口。

## 核心方法与创新机理

FICTION 的核心创新在于将“未来交互预测”从传统的 2D 空间或纯时序建模，系统性地迁移至**以 3D 场景为中心的多模态融合框架**。该方法通过显式引入 3D 环境上下文，同时解决了“在哪里交互”和“如何交互”这两个紧密耦合的子问题。相较于现有基线，其关键创新体现在以下三个 changed slots 上：

### 1. 输入表示：从 2D 视频到 3D 多模态融合

现有方法（如 **HierVL** 的自回归动作预测、**OCT** 的 2D 热图预测）仅依赖视频帧或 2D 空间信息，忽略了持久性的 3D 物体布局。FICTION 将输入扩展为三个模态的联合表示：**视频特征**（通过 EgoVLPv2 提取）、**3D 场景体素**（编码物体布局与演员位置）以及**人体姿态序列**（SMPL 参数）。这一设计的内在逻辑是：人类的活动意图与环境中物体的空间分布紧密耦合——例如，制作奶茶时，取水、加热、取杯等交互位置完全由水龙头、炉灶、杯架等物体的 3D 位置决定。仅凭 2D 视频无法捕捉这种 3D 空间约束。

### 2. 交互位置预测：从 2D 热图到 3D 体素网格

基线方法将交互位置预测建模为 2D 帧上的热图或自回归动作标签，这无法为后续的姿态预测提供精确的 3D 查询点。FICTION 将其重新定义为**3D 二元体素网格预测**：给定观察视频 $ \mathcal{V}_{0:\tau_o} $ 和场景点云 $ \mathcal{P} $，模型直接输出一个 $ N \times N \times N $ 的体素网格，其中每个体素标记该位置是否会在未来 $ \tau_f = 180 $ 秒内发生交互。这一 3D 输出天然地与场景几何对齐，使得模型能够区分垂直方向上的不同交互区域（如上层橱柜 vs. 下层抽屉）。消融实验提供了强有力的因果证据：**移除环境上下文后，Cooking 场景的 PR-AUC 从 21.0 骤降至 9.9**（Table 1），降幅超过 50%，证实了 3D 场景建模是性能提升的核心因果旋钮。

### 3. 姿态预测：从无环境条件的生成到位置查询的 CVAE

基线方法（如 **T2M-GPT-FT**、**4D-Humans**）将姿态预测视为无环境条件的自回归生成任务，无法针对特定交互位置产生差异化的姿态分布。FICTION 采用**基于位置查询的 CVAE 框架**：以多模态上下文表示 $ \bar{r} $ 和查询位置嵌入 $ \bar{x} $ 为条件，CVAE 编码器 $ E $ 从真实姿态中学习潜在分布参数 $ (\mu, \sigma) $，解码器 $ D $ 则从该分布中采样生成该位置特有的 SMPL 姿态参数 $ \theta $ 和位置 $ t $。这使得模型能够为同一场景中的不同交互位置生成截然不同的姿态——例如，从饮水机取水时使用双手，而从上层橱柜取物时需要伸展身体。在 Health 场景中，FICTION 的 MPJPE 比最佳基线 **T2M-GPT-FT** 低 49 mm（降幅 22.2%），验证了位置条件化对姿态预测精度的显著增益。

### 创新总结

三个 changed slots 形成了一条完整的因果链条：**3D 环境建模 → 精确的 3D 交互位置预测 → 位置条件化的多模态姿态生成**。这一链条的核心洞察是：未来交互的“在哪里”和“如何”必须被联合建模，且 3D 场景上下文是连接二者的关键桥梁。消融实验中环境移除导致的性能崩溃，以及跨三个场景（Cooking、Bike Repair、Health）超过 30% 的相对增益，共同构成了这一创新的决定性证据。

FICTION 的整体设计围绕一个核心命题展开：**未来交互的“在哪里”和“如何交互”必须耦合求解，且必须显式利用 3D 环境上下文**。为此，模型构建了一条从多模态输入到双任务输出的端到端预测管线，其架构如图 2 所示，可分为三个逻辑阶段。

### 多模态输入编码

模型接收三类异构输入，分别通过专用编码器映射到统一表示空间：

- **视频特征**：由预训练的 EgoVLPv2 提取，经 Visual Mapper (f_vm) 投影。
- **人体姿态序列**：以 SMPL 参数 $\theta$ 表示，经 Pose Mapper (f_pm) 编码。
- **3D 场景上下文**：包含场景体素（物体布局）与演员位置，经 Location Mapper (f_lm) 编码。

这三路特征随后被送入一个 Multimodal Transformer Encoder (L)，通过自注意力机制进行跨模态融合，生成上下文表示 $\bar{r}$。这一融合步骤是实现“环境-活动耦合”推理的关键——它使得模型能够在统一的表示空间中关联“人在哪里做了什么”与“环境中有什么物体”。

### 交互位置预测分支

位置预测分支从 $\bar{r}$ 出发，通过一个轻量的 Location Decoder (f_ld)（线性层）将融合表示映射为 $N^3$ 维向量，再重塑为 $N \times N \times N$ 的 3D 二元体素网格 $\hat{L}$。网格中每个体素的值为 1 或 0，分别指示该 3D 位置是否会在未来时间窗 $\tau_f$ 内发生对象交互。该分支的训练目标为二元交叉熵损失，直接监督模型学习“未来交互将发生在哪些 3D 位置”。

### 姿态预测分支（CVAE）

姿态预测分支采用条件变分自编码器（CVAE）架构，以解决“同一位置可能存在多种合理交互姿态”的多模态分布问题。其工作流程如下：

- **条件输入**：将融合表示 $\bar{r}$ 与查询位置 $\mathbf{x}_{\tau_k}$ 的嵌入拼接，作为 CVAE 的条件。
- **CVAE Encoder (E)**：在训练时，编码器接收条件输入与真实姿态 $P$，输出潜在分布参数 $\mu, \sigma$。
- **CVAE Decoder (D)**：从潜在变量 $z \sim \mathcal{N}(\mu, \sigma)$ 和条件中重建姿态参数 $\hat{P}$（包含 SMPL 参数 $\theta$ 与位置 $t$）。
- **推理时**：直接从标准正态分布 $\mathcal{N}(0,1)$ 采样 $z$，与条件拼接后经解码器生成姿态样本，从而获得该位置处的姿态分布。

训练损失由三项加权组成：

$$w_S \| P - \hat{P} \|_2 + w_J \| J - \hat{J} \|_1 + KL\left( \mathcal{N}(\mu, \sigma), \mathcal{N}(0,1) \right)$$

其中第一项为 SMPL 参数的 MSE 重建损失，第二项为 3D 关节位置的 L1 损失，第三项为潜在分布与标准正态的 KL 散度。这一设计使得模型既能精确重建训练样本，又能在推理时生成多样化的合理姿态。

### 输入输出流总结

整个管线的数据流可概括为：

1. **输入**：观察时间窗 $\tau_o = 30s$ 内的视频帧、对应的 SMPL 姿态序列、以及 3D 场景体素与演员位置。
2. **中间表示**：多模态 Transformer 编码器输出的融合上下文 $\bar{r}$。
3. **输出 1**：未来时间窗 $\tau_f = 180s$ 内的交互位置 3D 体素网格。
4. **输出 2**：给定查询位置下的未来交互姿态分布（SMPL 参数 $\theta$ 与位置 $t$ 的样本）。

值得注意的是，位置预测与姿态预测共享同一个多模态编码器，但在解码阶段解耦——位置分支仅需 $\bar{r}$，而姿态分支额外需要查询位置作为条件。这种“共享编码、解耦解码”的设计使得两个任务可以相互促进，同时保持各自的预测灵活性。

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the FICTION approach. The past observation information (video, pose, and environment) is encoded into a multimodal representation (left). The multimodal encoder L encodes the past observation, and is used to predict the interaction locations using a decoder (top right). We use the past observation encoding, along with the query location, to train a CVAE encoder decoder to generate a location-specific pose distribution conditioned on the past activity (bottom right)*

FICTION 的核心架构由三个功能模块构成：多模态编码与融合、交互位置预测、以及条件姿态生成。整个流程围绕一个关键设计展开——将 3D 场景上下文显式地注入到视频和人体姿态的表示学习中。

### 多模态编码与融合

模型接收三类异构输入：观察视频 $\mathcal{V}_{0:\tau_o}$、3D 场景体素（包含物体布局与演员位置）$\mathcal{P}$、以及 SMPL 姿态序列。这些输入分别经过专用编码器处理：

- **Video Encoder** ($f_V$)：采用 EgoVLPv2 提取视频帧级特征。
- **Visual Mapper** ($f_{vm}$)：将视频特征映射到统一的表示维度。
- **Pose Mapper** ($f_{pm}$)：编码 SMPL 姿态参数 $\theta$。
- **Location Mapper** ($f_{lm}$)：编码 3D 场景体素和演员位置。

上述编码后的多模态 token 被送入 **Multimodal Transformer Encoder** ($L$) 进行交叉注意力融合，最终输出一个紧凑的上下文表示 $\bar{r}$。该表示是整个模型的信息瓶颈——后续的位置预测和姿态生成均以其为条件。

### 交互位置预测

位置预测模块将上下文表示 $\bar{r}$ 解码为一个 $N \times N \times N$ 的二元体素网格 $\hat{L}$，其中每个体素标记为 1 表示该位置在未来 $\tau_f$ 时间窗内存在交互，0 表示不存在。解码器 $f_{ld}$ 是一个线性层，将 $\bar{r}$ 映射为 $N^3$ 维向量后 reshape 为体素网格。训练时使用二元交叉熵损失。

这一设计的形式化定义由未来对象交互函数给出：

$$\mathcal{F}_o\left(\mathcal{V}_{0:\tau_o}, \mathcal{P}\right) = \left\{ \mathbf{x}_{\tau_k} ~\vert~ \mathcal{T}(\mathbf{x}_{\tau_k}) \in \mathcal{O} \right\}$$

其中 $\mathcal{V}_{0:\tau_o}$ 为观察窗口内的视频，$\mathcal{P}$ 为 3D 位置集合，$\mathbf{x}_{\tau_k}$ 为未来交互发生的 3D 点，$\mathcal{T}(\cdot)$ 表示该点所属的物体类别，$\mathcal{O}$ 为目标物体集合。该函数的核心含义是：根据已观察的活动和场景布局，预测所有即将发生交互的 3D 位置。

### 条件姿态生成

对于每个预测出的交互位置，模型需要生成该位置处可能的人体姿态分布。这一任务由 **CVAE**（条件变分自编码器）完成：

- **CVAE Encoder** ($E$)：在训练时，接收上下文表示 $\bar{r}$、查询位置的嵌入 $\bar{x}$ 以及真实姿态 $P$，输出潜在分布的参数 $\mu, \sigma$。
- **CVAE Decoder** ($D$)：在推理时，从标准正态分布采样潜在变量 $z$，结合 $\bar{r}$ 和 $\bar{x}$ 作为条件，生成 SMPL 姿态参数 $\theta$ 和位置偏移 $t$ 的样本。

这一过程的形式化定义为未来交互姿态分布函数：

$$\mathcal{F}_p\left(\mathcal{V}_{0:\tau_o}, \mathcal{P}, \mathbf{x}_{\tau_k}\right) = \mathbb{P}(\theta, t)$$

该函数表示：给定观察视频、场景位置以及查询的交互点 $\mathbf{x}_{\tau_k}$，输出该点处 SMPL 姿态参数 $\theta$ 和人体位置 $t$ 的概率分布。CVAE 的引入使得模型能够捕捉同一交互位置下姿态的多模态性——例如，在水槽前可能弯腰洗手，也可能站立取水。

### 训练损失

CVAE 的训练损失由三项加权组合而成：

$$w_S \| P - \hat{P} \|_2 + w_J \| J - \hat{J} \|_1 + KL\left(\mathcal{N}(\mu, \sigma), \mathcal{N}(0, 1)\right)$$

- 第一项为 SMPL 参数 $P$ 的均方误差（MSE），约束生成姿态的全局合理性。
- 第二项为 3D 关节位置 $J$ 的 L1 误差，直接监督末端关节的空间精度。
- 第三项为 KL 散度，迫使潜在分布 $\mathcal{N}(\mu, \sigma)$ 趋近标准正态分布 $\mathcal{N}(0, 1)$，保证推理时采样的有效性。

$w_S$ 和 $w_J$ 为两项重建损失的权重。位置预测模块的 BCE 损失与 CVAE 损失联合优化，实现“在哪里交互”和“如何交互”的端到端学习。

## 实验与关键发现

FICTION 在 Ego-Exo4D 数据集的三个场景（Cooking、Bike Repair、Health）上进行了全面的定量和定性评估。测试集的环境从未在训练中出现，确保跨场景泛化能力的公平评估。以下从交互位置预测、姿态预测、消融实验和定性分析四个维度展开。

### 交互位置预测

Table 1（左）报告了未来交互位置预测的结果，指标包括 Precision-Recall AUC（PR-AUC）和 Chamfer Distance（Ch↓）。FICTION 在所有场景上均显著优于现有方法。在 Cooking 场景，FICTION 的 PR-AUC 达到 21.0，较最佳基线 **OCT** 的 16.9 提升 4.1 个绝对点（相对增益 24.3%）；Chamfer Distance 从 9.0 降至 7.4。在 Bike Repair 场景，PR-AUC 为 18.7（OCT 为 14.1），在 Health 场景同样保持领先。综合来看，FICTION 在 PR-AUC 上的相对增益超过 32%（绝对 4.6%），证明了将 3D 环境上下文显式融入预测框架的有效性。

### 姿态预测

Table 1（右）报告了未来交互姿态预测的结果，指标包括 MPJPE 和 PA-MPJPE。FICTION 在所有场景上均超越所有基线方法。以 MPJPE 为例，在 Cooking 场景，FICTION 达到 229mm，较微调后的 **T2M-GPT-FT**（264mm）降低 35mm（13.3%）；在 Health 场景，FICTION 达到 172mm，较 T2M-GPT-FT（221mm）降低 49mm（22.2%）。这一显著提升表明，基于位置查询的 CVAE 能够有效利用多模态上下文，生成更准确的条件化姿态分布。

### 消融实验

消融实验系统性地验证了各组件和超参数对性能的影响：

- **环境上下文的关键性**：移除 3D 环境输入（FICTION w/o env）导致 Cooking 场景的位置预测 PR-AUC 从 21.0 骤降至 9.9，降幅超过 50%。这直接证实了显式 3D 场景建模是任务的核心驱动力，而非辅助信息。移除视频或姿态输入虽导致性能下降，但模型仍可基于剩余模态保持一定预测能力，说明多模态融合具有互补性和冗余容错能力。

- **观察时间窗口 τ_o**：Table 2 显示，τ_o = 30 秒在提供足够活动上下文和计算效率之间取得最佳平衡。当 τ_o = 0 秒（无历史观察）时，性能显著下降，表明模型确实从过去行为中提取了有效时序信息。

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/007_Table_2.jpg]]
*Table 2: Effect of*

- **未来时间窗口 τ_f**：Table 3 探究了预测窗口长度的影响，验证了模型在长时预测（3 分钟）下的稳定性。

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/008_Table_3.jpg]]
*Table 3: Effect of*

- **模型容量**：Table 5 表明，将 Transformer 编码器层数从 2 增至 6 持续提升性能，说明任务对模型容量有较高需求，更大的模型可能带来进一步收益（需手动验证 6 层以上是否收敛）。

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/010_Table_5.jpg]]
*Table 5: Effect of the model size on the performance. We vary the number of transformer layers*

- **学习率敏感度**：Table 4 展示了不同学习率对性能的影响，为超参数选择提供了实证依据。

### 定性分析

Figure 4 展示了 FICTION 的定性预测结果。在 Cooking 场景中，模型根据观察到的自我中心视频，正确预测了未来交互位置——冰箱、水龙头、橱柜，且空间分布与真实活动流程一致。在 Bike Repair 场景中，若观察序列显示人物正在修理轮胎，模型预测轮胎将在后续阶段被安装到自行车上，空间位置发生合理迁移。Figure 5 进一步将 FICTION 与基线方法进行可视化比较，FICTION 的预测在交互位置的准确性和姿态的自然度上均明显优于基线。

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of example results. (Top) Interaction location prediction in a cooking take. Based on the observed input ego, the model is able to correctly predict future interaction locations— refrigerator, faucet, cabinet. (Middle, bottom): Interaction sequences in a cooking and a bike repair take. Given the past observation information, our model is able to accurately predict future interactions. If the observed sequence shows the person fixing the tire, the model predicts that the tire will be fixed onto the bike at a later stage, at a different spatial location (bottom, left most pose visualization). Best viewed in zoom. Exo view shown for visualization only*

![[assets/figures/papers/paper_list_l24_FIction_4D_Future_Interaction_Prediction_from_Video/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of our method with baselines and a cooking (left) and a bike-repair (right) take*

### 局限性与失败模式

尽管 FICTION 取得了显著性能提升，仍存在以下局限：

1. **单人假设**：模型假设每个视频仅包含一个演员，无法显式处理多人协作或交互场景。
2. **静态场景假设**：数据集构建时假设点云为静态，而实际环境中物体位置可能随时间变化（如移动椅子），这会导致交互位置预测的偏差。
3. **数据集构建依赖**：交互实例的标注依赖 Detic 检测器、WHAM 姿态估计和 Llama 3.1 语言模型，这些上游模型的误差会传播至训练数据，影响模型质量。未来改进上游组件将有望进一步提升 FICTION 的性能。

## 定位与知识库关联

### 任务定义与问题边界

FICTION 将未来交互预测定义为一个双输出问题：给定过去 $\tau_o$ 秒的第一人称视频 $\mathcal{V}_{0:\tau_o}$ 和包含演员与物体的 3D 场景点云 $\mathcal{P}$，同时预测（1）未来 $\tau_f$ 秒内所有物体交互发生的 3D 位置集合 $\mathcal{F}_o$，以及（2）每个查询位置 $\mathbf{x}_{\tau_k}$ 处的人体姿态分布 $\mathcal{F}_p$（SMPL 参数 $\theta$ 与 3D 平移 $t$）。交互被严格定义为“手部进入物体 3D 包围盒且 LLM 判定为接触式操作”的时刻，排除监控、观察等非接触行为。

该定义将任务从传统 2D 动作预测或 3D 姿态预测的单一输出空间，提升到“在哪里交互 + 如何交互”的联合 4D 空间，要求模型同时具备场景理解、活动推理和姿态生成能力。

### 方法谱系中的位置

**相对于 2D 动作预测方法**：HierVL 等自回归动作预测模型仅输出 2D 动作标签序列，缺乏空间定位能力。FICTION 通过 3D 体素网格显式预测交互位置，将“何时发生什么动作”拓展为“在 3D 场景的何处、以何种姿态发生交互”，填补了 2D 时序预测与 3D 空间理解之间的鸿沟。

**相对于 2D 热图提升方法**：OCT 从 2D 交互热图提升到 3D，但本质上仍依赖 2D 帧内线索，缺乏对持久性 3D 环境上下文（物体布局、空间关系）的建模。FICTION 直接将 3D 场景体素作为输入模态之一，使模型能够学习“冰箱在角落→取食材的交互位置靠近冰箱”这类空间约束。消融实验证实，移除环境上下文后，Cooking 场景的 PR-AUC 从 21.0 骤降至 9.9（Table 1），降幅超过 50%，说明 2D 提升方法的根本瓶颈正在于缺失 3D 场景先验。

**相对于 3D 占用预测方法**：OccFormer 和 VoxFormer 从视频预测 3D 占用网格，但目标是重建当前场景几何，而非预测未来交互。FICTION 借鉴了视频到 3D 的映射思想，但将输出重新定义为“未来交互概率体素”，并通过多模态 Transformer 融合视频、姿态和场景信息，实现了从静态场景理解到动态交互预测的跨越。

**相对于自回归姿态预测方法**：4D-Humans 和 T2M-GPT 可生成未来人体姿态序列，但缺乏环境条件化——它们不知道人在厨房还是修车铺，因此无法根据场景上下文调整姿态（例如，在灶台前弯腰炒菜 vs. 在自行车旁蹲下修轮胎）。FICTION 的 CVAE 以查询位置和场景上下文为条件生成姿态分布，使姿态预测与具体交互位置绑定。在 Health 场景，FICTION 的 MPJPE 比微调后的 T2M-GPT-FT 低 49 mm（22.2%），直接证明了环境条件化的增益。

**相对于通用视频到姿态 CVAE**：Video-to-pose CVAE 仅以视频为条件，缺失 3D 位置查询机制。FICTION 通过“先定位、后生成”的两阶段设计，将位置预测与姿态生成解耦，使 CVAE 可以专注于学习“给定位置和上下文时的姿态多模态分布”，避免了单阶段模型需要同时优化两个异构目标的困难。

### 适用边界

**场景泛化**：实验在 Ego-Exo4D 的 Cooking、Bike Repair、Health 三个场景上进行，测试集环境从未在训练中出现。模型在这三类程序性活动上表现一致，但数据集构建假设静态点云（物体位置不随时间变化），对于物体频繁移动的场景（如搬家、整理货架），当前方法可能失效。

**单演员假设**：FICTION 假设每个视频仅有一个演员。在多人协作场景（如双人搬家具、手术室团队操作）中，模型无法区分不同人的交互意图和姿态，需扩展为多实例预测框架。

**观察时长依赖**：消融实验（Table 2）表明，观察时间 $\tau_o=30$ 秒提供足够的活动上下文；当 $\tau_o=0$（仅使用当前帧）时性能显著下降。这意味着模型不适合零观察的即时预测，需要一定长度的历史视频来推断活动进度和未来意图。

**模型容量上限未探明**：Transformer 层数从 2 增加到 6 持续提升性能（Table 5），暗示当前模型容量尚未饱和，更大模型可能带来进一步增益，但计算成本与实时性之间的权衡需要在实际部署中评估。

### 局限与开放问题

**数据构建的级联误差**：交互实例的标注依赖 Detic（物体检测）、WHAM（手部姿态估计）和 Llama 3.1（叙述-物体匹配）三个预训练模型。任一环节的误差都会传播到训练标签中，影响模型学习质量。论文承认这一点，但未量化各环节的误差贡献。

**动态场景处理**：当前假设场景点云在 $\tau_f=180$ 秒内保持静态。实际中，椅子被拉出、工具被取走等物体位移会改变可交互位置的空间分布。如何将动态物体跟踪融入预测管线是一个开放方向。

**多人扩展**：将模型从单演员推广到多人场景，需要解决交互归属（谁将交互哪个物体）、姿态解耦（多人姿态不碰撞）和社交上下文建模（协作或竞争关系影响交互序列）等问题。

**流式与在线修正**：当前模型离线处理固定长度的观察窗口。在 AR 辅助等应用中，需要流式输入并随着新观测实时修正未来预测。这涉及时序模型架构的重新设计，以及预测置信度的在线估计。

**更广泛的活动类型**：三个测试场景均为结构化程序性活动（有明确的步骤顺序）。对于非结构化活动（如自由玩耍、社交聚会），交互的定义和预测逻辑可能需要根本性调整——交互不再遵循固定程序，而是由社交线索和即时意图驱动。

## 原文 PDF

![[paperPDFs/CVPR_2025/FIction_4D_Future_Interaction_Prediction_from_Video.pdf]]
