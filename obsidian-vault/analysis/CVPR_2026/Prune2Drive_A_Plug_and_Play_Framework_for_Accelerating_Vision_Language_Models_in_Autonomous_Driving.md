---
title: "Prune2Drive: A Plug-and-Play Framework for Accelerating Vision-Language Models in Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Prune2Drive_A_Plug_and_Play_Framework_for_Accelerating_Vision_Language_Models_in_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/MinhaoXiong/Prune2Drive.git"
aliases:
- Prune2Drive
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Prune2Drive
primary_logic: Prune2Drive
claims:
- Prune2Drive
---

# Prune2Drive: A Plug-and-Play Framework for Accelerating Vision-Language Models in Autonomous Driving

> [!tip] 核心洞察
> Prune2Drive

| 字段 | 内容 |
|------|------|
| 中文题名 | Prune2Drive: A Plug-and-Play Framework for Accelerating Vision-Language Models in Autonomous Driving |
| 英文题名 | Prune2Drive: A Plug-and-Play Framework for Accelerating Vision-Language Models in Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.13305) · [Code](https://github.com/MinhaoXiong/Prune2Drive.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method |  |
| Dataset | DriveLM, DriveLMM-o1, MME, OmniDrive, nuScenes |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

自动驾驶视觉语言模型（VLM）依赖多视角图像输入进行场景理解与决策，但多视角带来的大量视觉 token 导致自注意力的二次复杂度 $O(N^2)$ 成为推理效率的核心瓶颈。现有 token 压缩方法（如 FastV、DART）在自动驾驶场景下存在两个关键缺陷：一是忽略多视角间的语义与空间多样性，导致重要目标被错误丢弃；二是对所有视角采用统一的压缩比，无法自适应不同视角的信息密度差异。

**Prune2Drive** 是一个即插即用的多视角视觉 token 剪枝框架，通过两个核心组件解决上述问题：

1. **多样性感知的 token 选择机制（T-FPS）**：受最远点采样启发，在 token 嵌入空间中基于余弦距离选择最具代表性的视觉 token，同时保留语义覆盖与空间分布多样性。
2. **视角自适应剪枝比例优化**：在验证子集上自动搜索各视角的最优 token 保留比例，通过奖励-惩罚目标函数平衡任务性能与 token 使用量。

在 DriveLM 和 DriveLMM-o1 两个自动驾驶 VLM 基准上，Prune2Drive 仅保留约 10% 的视觉 token 即可实现：预填充阶段 **6.40× 加速**，仅消耗 **13.4% FLOPs**，同时平均性能下降控制在 **3%** 以内，达到该设定下的最优结果。方法无需重新训练底层 VLM，收敛仅需约 3 个 H100 GPU 小时，展现出良好的实用性与可部署性。



视觉语言模型（VLMs）正逐渐成为自动驾驶（AD）感知与决策的核心组件，尤其是在多视图输入场景下，模型需要同时处理来自前视、后视、侧视等多个摄像头的视觉信息。然而，VLM 的自注意力机制具有关于序列长度 $N$ 的 $\mathcal{O}(N^2)$ 计算复杂度，当多视图的高分辨率图像被转换为大量视觉 token 后，推理延迟和显存占用急剧膨胀，严重制约了实时部署的可行性。

现有 token 压缩方法（如 FastV 等）在多视图场景下暴露出两个关键缺陷。其一，它们通常对所有视图采用统一的压缩策略，忽略了不同摄像头视角对驾驶决策的差异化贡献——例如前视图通常比侧视图包含更多安全关键信息。其二，压缩过程中缺乏对 token 语义与空间多样性的显式保护，容易丢弃远处小目标或边缘区域的重要线索，导致场景理解出现事实性错误。如 Figure 1 所示，FastV 错误地将前视图中的白色货车描述为“摩托车骑手”，而 Prune2Drive 则通过保留语义和空间上更具代表性的 token 正确识别了该目标。

针对上述瓶颈，本文提出 **Prune2Drive**，一个即插即用的多视图 VLM 视觉 token 剪枝框架。其核心动机在于：通过**视图自适应**的剪枝比例分配与**多样性感知**的 token 选择，在显著降低计算开销的同时，最大限度地保留对驾驶决策关键的多视图信息。具体而言，Prune2Drive 在 DriveLM 基准上仅消耗 13.4% 的 FLOPs 即可将平均性能下降控制在约 3%，并在预填充阶段实现 6.40× 的加速比，同时达到 SOTA 水平。



## 核心方法与创新机理

Prune2Drive 的核心创新在于将多视图视觉 token 剪枝从“均匀压缩”或“单视图注意力筛选”推进到 **“多样性保持 + 视图自适应”** 的双阶段联合优化框架。其 changed slots 集中体现在两个关键模块上：

### 1. 多样性感知的 Token 剪枝策略（T-FPS）

传统 token 压缩方法（如 FastV）通常基于注意力分数进行剪枝，容易保留语义冗余的 token，而忽视跨视图的空间覆盖完整性。Prune2Drive 将剪枝问题建模为 **k-center 贪心求解**，提出 **T-FPS（Token Farthest Point Sampling）** 算法：在 token 嵌入空间中，以余弦距离为度量，迭代选择与已保留集合距离最远的 token，从而最大化被保留 token 集合对原始语义空间的覆盖。

- **瓶颈定位**：多视图 VLM 中，自注意力的二次复杂度 $\mathcal{O}(N^2)$ 是推理延迟的主要瓶颈，而不同视图之间存在大量空间和语义冗余。
- **因果旋钮**：T-FPS 直接作用于视觉编码器输出的 token 序列，通过贪心选择非冗余 token，在保持语义和空间多样性的前提下大幅减少进入 LLM 的 token 数量。
- **效率优势**：对于每张图 $N=729$ 个 token 的典型配置，T-FPS 仅需约 **0.02 秒**，FLOPs 占比不到总体的 **0.1%**，几乎不引入额外计算开销。

### 2. 视图自适应的剪枝比例优化

多视图自动驾驶场景中，不同相机视角对决策任务的重要性天然存在差异（例如前视图通常比侧后视图包含更多关键信息）。现有方法对所有视图施加统一的剪枝比例，导致重要视图信息丢失或冗余视图资源浪费。

Prune2Drive 引入一个 **奖励-惩罚目标函数**，在验证集上自动搜索每个视图的最优 token 保留比例 $\boldsymbol{\alpha}^*$：

$$\boldsymbol{\alpha}^{\ast} = \arg \max_{\boldsymbol{\alpha} \in \mathcal{A}} \mathcal{M}(\boldsymbol{\alpha}; \mathcal{D}_{\mathrm{val}}, \mathcal{W})$$

$$\mathcal{M}(\boldsymbol{\alpha}) = R(\boldsymbol{\alpha}) - \lambda P(\boldsymbol{\alpha})$$

其中 $R$ 为任务性能奖励，$P$ 为 token 使用量的惩罚项，$\lambda$ 控制性能与效率的权衡。搜索仅在随机采样的小规模验证子集上进行，冻结 VLM 权重，约 **3 个 H100 GPU 小时**即可收敛。

- **理论支撑**：论文从视角加权的 Lipschitz 连续性出发，证明了预测误差上界由各视图的 Hausdorff 距离加权和所控制——T-FPS 最小化单视图信息损失，而视图自适应优化则将更多预算分配给内在重要性更高的视图，直接压制误差上界中的主导项。
- **证据强度**：消融实验（Table 6/7）表明，移除视图自适应优化或替换 T-FPS 为随机/注意力剪枝均会导致显著性能下降，验证了两个模块的独立贡献与协同效应。

### 与 Baseline 的本质差异

| 维度 | FastV 等现有方法 | Prune2Drive |
|------|-----------------|-------------|
| 剪枝依据 | 注意力分数（易冗余） | 嵌入空间多样性（k-center） |
| 视图策略 | 统一剪枝比例 | 视图自适应优化 |
| 优化目标 | 启发式规则 | 奖励-惩罚联合优化 |
| 即插即用性 | 需修改模型结构 | 无需微调 VLM 权重 |



Prune2Drive 的整体 pipeline 围绕“视觉 token 裁剪”这一核心操作展开，其设计目标是在不修改 VLM 内部参数的前提下，以即插即用的方式大幅降低多视图输入带来的计算开销。框架由两条正交但协同的支路构成：**视图自适应裁剪比例优化**（view-adaptive pruning ratio optimization）和**多样性感知的 token 选择策略 T-FPS**（diversity-aware token pruning via Farthest Point Sampling）。

### Pipeline 总览

图 3 给出了完整的架构示意。给定一个多视图 VLM 模型 $\mathcal{W}$（参数冻结）和一组来自 $M$ 个相机视角的视觉 token 序列 $\{\mathbf{V}_i\}_{i=1}^{M}$，Prune2Drive 的处理流程如下：

1. **比例决策阶段**：视图自适应优化模块输出一个裁剪比例向量 $\boldsymbol{\alpha}^* = (\alpha_1, \alpha_2, \dots, \alpha_M)$，其中 $\alpha_i \in (0, 1]$ 表示第 $i$ 个视图应保留的 token 比例。该向量通过在一个小型验证集 $\mathcal{D}_{\mathrm{val}}$ 上最大化目标函数 $\mathcal{M}(\boldsymbol{\alpha}) = R(\boldsymbol{\alpha}) - \lambda P(\boldsymbol{\alpha})$ 得到——$R$ 衡量下游任务性能，$P$ 惩罚 token 使用量，$\lambda$ 控制二者的权衡。

2. **Token 选择阶段**：对每个视图 $i$，T-FPS 算法从 $\mathbf{V}_i \in \mathbb{R}^{N \times d}$ 中选出 $K_i = \lceil \alpha_i N \rceil$ 个 token，形成裁剪后的集合 $\mathbf{S}_i$。选择依据是 token 嵌入空间中的余弦距离，通过贪心 k-center 求解确保保留的 token 在语义和空间上最大化覆盖原始分布。

3. **推理阶段**：裁剪后的 token 序列 $\{\mathbf{S}_i\}$ 与文本 token 拼接后送入 LLM 主干，完成后续的注意力计算与生成。由于视觉 token 数量从 $M \times N$ 降至 $\sum_i K_i$，自注意力的 $\mathcal{O}(N^2)$ 复杂度在预填充阶段得到显著压缩。

### 模块关系与信息流

两个核心模块之间存在明确的因果分工：

- **视图自适应优化**解决的是“每个视图该留多少 token”的**宏观预算分配**问题。它隐式地学习了各视图对下游任务的内在重要性权重 $w_i$，将更多预算分配给高重要性的视角（如正前方），从而在理论层面最小化由裁剪引起的加权 Hausdorff 误差上界 $\sum_i w_i \cdot d_H(\mathbf{V}_i, \mathbf{S}_i)$。
- **T-FPS** 解决的是“给定预算后该选哪些 token”的**微观选择**问题。作为贪心 k-center 求解器，它保证 $d_H(\mathbf{V}_i, \mathbf{S}_i)$ 在每视图内部尽可能小，从而将信息损失控制在局部最优水平。

这种“先分配、后选择”的解耦设计使得框架可以灵活适配不同的 VLM 架构和任务场景：比例优化只需在验证集上运行一次（约 3 个 H100 GPU 小时即可收敛），而 T-FPS 在推理时对每张图（$N=729$ 个 token）仅需约 0.02 秒，额外计算量不足总 FLOPs 的 0.1%。二者均不涉及对 VLM 权重的任何微调或梯度回传，因此 Prune2Drive 天然具备即插即用特性。

### 补充图表

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/003_Figure_3.jpg]]
*Figure 3: Detailed architecture of Prune2Drive. (a) VLM workflow in Prune2Drive, (b) View-adaptive pruning ratio optimization, where view-specific token pruning ratios are automatically determined, and (c) Diversity-aware T-FPS token pruning strategy, which preserves visual tokens that contain rich semantic and spatial information across multi-view inputs*



Prune2Drive 由两个关键模块构成：**多样性感知的 T-FPS 令牌剪枝策略** 和 **视角自适应剪枝比例优化框架**。两者协同工作，在预填充阶段对多视图视觉令牌进行高效压缩。

### 3.1 多样性感知令牌剪枝 (T-FPS)

T-FPS（Token Farthest Point Sampling）是一种轻量级的令牌剪枝方法，其核心思想源于最远点采样（FPS）在点云处理中的成功应用。给定来自某一视图的视觉令牌序列 $\mathbf{V} \in \mathbb{R}^{N \times d}$（$N$ 为原始令牌数，$d$ 为嵌入维度），T-FPS 的目标是选出一个大小为 $K$ 的子集 $\mathbf{S}$，使得被保留的令牌在语义空间中具有最大的覆盖范围。

算法以贪婪 k-center 求解器的方式运作：首先随机选取一个初始令牌，然后迭代地选择与已选集合余弦距离最远的令牌加入 $\mathbf{S}$，直至选出 $K$ 个令牌。其核心距离度量采用 **令牌嵌入空间中的余弦距离**，而非原始像素空间距离，这使得算法能够感知语义层面的冗余性。

**计算开销极小**：对于每张图像 $N=729$ 个令牌的典型设置，T-FPS 仅需约 0.02 秒，占模型总 FLOPs 的不到 0.1%，可视为零开销的即插即用模块。

### 3.2 视角自适应剪枝比例优化

自动驾驶场景中，不同相机视角的重要性天然存在差异（例如前视图通常比后视图包含更多关键信息）。为捕捉这种非对称性，Prune2Drive 引入了一个自动搜索框架，为 $M$ 个视角分别分配独立的令牌保留比例 $\alpha_i$，构成向量 $\pmb{\alpha} = [\alpha_1, \alpha_2, \dots, \alpha_M]$。

**优化目标**：在验证集 $\mathcal{D}_{\mathrm{val}}$ 上，冻结 VLM 参数 $\mathcal{W}$，通过最大化如下奖励-惩罚目标函数来搜索最优保留比例：

$$\pmb{\alpha}^{\ast} = \arg \operatorname*{max}_{\pmb{\alpha} \in \mathcal{A}} \mathcal{M}(\pmb{\alpha}; \mathcal{D}_{\mathrm{val}}, \mathcal{W})$$

其中目标函数 $\mathcal{M}$ 定义为：

$$\mathcal{M}(\pmb{\alpha}) = R(\pmb{\alpha}) - \lambda P(\pmb{\alpha})$$

- $R(\pmb{\alpha})$：任务性能奖励项，衡量在保留比例 $\pmb{\alpha}$ 下模型的推理质量；
- $P(\pmb{\alpha})$：令牌使用惩罚项，与总保留令牌数正相关；
- $\lambda$：**权衡超参数**，控制性能保持与计算压缩之间的平衡。$\lambda$ 越大，优化结果越倾向于激进剪枝（更少令牌、更低计算量）；$\lambda$ 越小，则越倾向于保守剪枝（更多令牌、更高性能保持）。

搜索在一个从完整训练集中随机采样的小规模代表性子集上进行，整个优化过程在 3 个 H100 GPU 小时内即可收敛，搜索成本可控。

### 3.3 理论保证：视角加权 Lipschitz 连续性

论文从理论上证明了 Prune2Drive 两个模块设计的合理性。假设 VLM 的推理函数 $f$ 关于输入令牌集满足某种 Lipschitz 连续性，则模型预测 $y$ 与剪枝后预测 $\hat{y}$ 之间的误差存在上界：

$$\| y - \hat{y} \| \leq C_f \sum_{i=1}^{M} w_i \cdot d_H(V_i, S_i)$$

其中：
- $C_f$ 是模型相关的 Lipschitz 常数；
- $w_i$ 是第 $i$ 个视角的内在重要性权重；
- $d_H(V_i, S_i)$ 是原始令牌集 $V_i$ 与剪枝后令牌集 $S_i$ 之间的 **Hausdorff 距离**，定义为：

$$d_H(V_i, S_i) := \max \Bigl\{ \sup_{v \in V_i} \inf_{s \in S_i} d(v, s),\ \sup_{s \in S_i} \inf_{v \in V_i} d(v, s) \Bigr\}$$

该距离度量了剪枝造成的最大信息损失。

**两个模块的协同作用**由此清晰呈现：
- **T-FPS** 作为贪婪 k-center 求解器，确保保留令牌 $S_i$ 最大程度覆盖语义空间 $V_i$，从而最小化每视角的信息损失 $d_H(V_i, S_i)$；
- **视角自适应优化** 则策略性地将更大的令牌预算分配给内在重要性 $w_i$ 更高的视角，直接减小加权误差总和中的主导项。

这一理论框架为 Prune2Drive 的“多样性保留 + 视角差异化分配”设计提供了形式化支撑。

### 补充图表

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/001_Figure.jpg]]
*Figure: FastV: There is a person riding a motorcycle to the front of the ego vehicle, a white straight arrow to the front of the ego vehicle, and a black traffic sign to the back of the ego vehicle. Ours: There is a white van to the front of the ego vehicle, a black sedan to the back of the ego vehicle, and a person riding a motorcycle to the front of the ego vehicle*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/011_Figure_4.jpg]]
*Figure 4: Quantitative results of selected visual tokens. We compare selected visual tokens by FastV, DART and Prune2Drive. The red box indicates the position bias of attention-based token-pruning method, where posterior tokens are retained, and the green bounding boxes highlight critical objects captured by Prune2Drive, which enables view-importance assignment and diversity-aware token selection*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/014_Figure_5.jpg]]
*Figure 5: Quantitative results of selected visual tokens. We compare selected visual tokens by FastV, DART, and Prune2Drive. FastV shows position bias (red boxes), retaining mostly posterior tokens, DART neglects view importance, while our Prune2Drive (green boxes) captures critical objects through view-importance and diversity-aware selection*



## 实验与关键发现

### 主实验结果

Prune2Drive 在自动驾驶视觉语言模型（VLM）的两个核心基准上展现出显著的效率-精度权衡优势：在 **DriveLM** 基准上，当保留 180 个 token/图（75% 剪枝率）时，使用 DriveMM 模型取得 58.3 平均分，仅比全 token 模型下降约 1%；进一步保留 72 个 token/图（90% 剪枝率）时仍取得 57.4 平均分。在 **DriveLMM-o1** 基准上，75% 和 90% 剪枝率下的整体推理得分分别为 69.3 和 68.3，均优于其他 token 压缩方法。

效率方面，Prune2Drive 在 prefilling 阶段实现 **6.40× 加速**，FLOPs 消耗仅占原始的 **13.4%**（DriveLM）和 **20.3%**（DriveLMM-o1），同时平均性能下降控制在 3% 和 6%。在通用 VLM 基准 **MME** 上，保留 128 token（22.2% 原始量）即可达到全 token 性能的 **97.3%**，验证了方法的跨任务泛化能力。

与现有 token 压缩方法的对比实验（Table 1，Table 2）表明，无论是 FastV 这类基于注意力分数的剪枝方法，还是其他压缩策略，Prune2Drive 在同等剪枝率下均取得最优性能。在视频自动驾驶基准 **OmniDrive** 上的实验（Table 5）进一步验证了方法在时序场景中的有效性。

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/004_Table_1.jpg]]
*Table 1: Comparison with other token compression methods on DriveLM benchmark using DriveMM model*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/005_Table_2.jpg]]
*Table 2: Comparison with other token compression methods on DriveLMM-o1 using DriveLMM-o1 model*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/008_Table_5.jpg]]
*Table 5: Comparison on the Video AD benchmark OmniDrive*

### 消融实验

消融实验围绕两个核心组件展开（Table 6，Table 7）：

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/009_Table_6.jpg]]
*Table 6: Ablation Studies on DriveLMM-o1 benchmark*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/010_Table_7.jpg]]
*Table 7: Ablation Studies on DriveLM benchmark*

**T-FPS 多样性剪枝策略的有效性**：与随机剪枝、基于注意力分数的 Top-K 剪枝相比，T-FPS 在相同保留 token 数下性能始终最优。这源于其作为贪心 k-center 求解器的特性——通过余弦距离在 token 嵌入空间中最大化语义覆盖，从而最小化 Hausdorff 距离定义的信息损失。

**视角自适应剪枝比优化的贡献**：将固定均匀剪枝比替换为视角自适应优化后，性能有显著提升。理论分析表明，视角自适应分配本质上是对视角重要性权重 $w_i$ 的高效响应——对重要性高的视角分配更多 token 预算，直接降低加权误差和中的主导项。

**计算开销**：T-FPS 算法对 $N=729$ token/图的处理仅需 **0.02 秒**，占总体 FLOPs 不足 **0.1%**；视角自适应优化在 H100 GPU 上约 **3 小时** 即可收敛，且搜索仅需从训练集中随机采样的少量代表性验证子集 $D_{val}$。

### 关键超参数分析

**权衡超参数 $\lambda$** 控制奖励函数 $R(\alpha)$ 与 token 使用惩罚 $P(\alpha)$ 之间的平衡。Table 9 的敏感性分析表明，$\lambda$ 在合理范围内变化时性能波动平缓，方法对该参数不敏感，便于实际部署。具体优化超参数设置见 Table 8。

### 失败模式与局限性

虽然 Prune2Drive 在多数场景下表现优异，但以下局限性需注意：

1. **极端剪枝率下的退化**：当剪枝率超过 90% 时，性能下降加速，尤其在需要细粒度空间推理的任务（如小目标检测相关描述）上表现更明显。这符合理论预期——Hausdorff 距离上界在 token 数过少时难以维持紧凑。

2. **视角重要性静态假设**：视角自适应优化基于验证集 $D_{val}$ 搜索得到固定比率 $\alpha^*$，未考虑推理时场景动态变化。在极端视角遮挡或传感器故障场景下，静态分配可能次优。

3. **VLM 架构依赖**：T-FPS 依赖视觉编码器输出的 token 嵌入质量，若底层视觉编码器对某些视角的表示能力不足，多样性采样可能放大该缺陷。

4. **基准覆盖有限**：当前实验主要在 DriveLM、DriveLMM-o1 和 OmniDrive 上进行，缺乏在更多真实驾驶场景（如复杂天气、夜间条件）下的系统性验证，该结论需手动核实。

### 补充图表

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/006_Table_3.jpg]]
*Table 3: Regular VLM benchmarks*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/012_Table_8.jpg]]
*Table 8: Hyperparameters in pruning ratio optimization*

![[assets/figures/papers/paper_list_l777_https_arxiv_org_abs_2508_13305/figures/013_Table_9.jpg]]
*Table 9: Sensitivity of λ*



## 定位与知识库关联

### 1. 与现有视觉Token压缩方法的关系

Prune2Drive 定位于多视图视觉语言模型（VLM）的高效推理赛道，其核心贡献在于将 **多样性保持** 和 **视图自适应** 两个维度引入视觉 token 剪枝，与现有方法形成差异化。

#### 1.1 与通用Token剪枝方法的对比

论文在 DriveLM 和 DriveLMM-o1 两个自动驾驶基准上将 Prune2Drive 与以下方法进行了系统对比（参见 Table 1 和 Table 2）：

- **FastV**：一种基于注意力分数进行 token 丢弃的方法。Prune2Drive 在 Figure 1 中展示了定性对比——FastV 倾向于保留注意力高分区域，但可能遗漏关键小目标（如前方摩托车），而 Prune2Drive 的 T-FPS 策略通过语义空间覆盖更完整地捕捉了重要物体。在 75% 剪枝率下，Prune2Drive 在 DriveLM 上达到 58.3 平均分，性能下降仅约 1%（相对于全量 token 模型），显著优于 FastV 等基线。
- 其他对比方法包括基于 **token 合并（merging）** 和 **token 下采样（downsampling）** 的策略。Table 1 和 Table 2 显示，在同等 token 保留率下，Prune2Drive 在两个基准上均取得最优综合性能。

#### 1.2 方法谱系中的位置

Prune2Drive 的两个核心模块可追溯到不同的技术脉络：

- **T-FPS（Token Farthest Point Sampling）**：灵感来源于点云处理中的最远点采样（Farthest Point Sampling），论文将其迁移到 token 嵌入空间，以余弦距离作为度量，等价于贪心 k-center 求解器。该方法与基于聚类的 token 压缩方法（如 K-Means 聚类后取中心点）有本质区别——T-FPS 直接选取原始 token 子集，保留了 token 的原始语义完整性，且计算开销极低（0.02 秒处理 729 个 token，占模型总 FLOPs 不足 0.1%）。
- **视图自适应剪枝率优化**：该模块将每个相机视图的 token 保留率作为可优化变量，通过在验证集上最大化奖励-惩罚目标函数 $\mathcal{M}(\pmb{\alpha}) = R(\pmb{\alpha}) - \lambda P(\pmb{\alpha})$ 来搜索最优分配。这一思路与 AutoML 中的超参数搜索和神经架构搜索（NAS）有方法论上的亲缘关系，但其搜索空间限定在视图级别的保留率向量，收敛仅需 3 H100 GPU 小时，远轻量于传统 NAS。

### 2. 理论支撑与适用边界

#### 2.1 理论保证

论文在 §3.3 提供了基于 **视图加权 Lipschitz 连续性** 的理论分析。核心结论是：预测误差被各视图 Hausdorff 距离的加权和所上界控制：

$$\| y - \hat{y} \| \leq C_f \sum_{i=1}^{M} w_i \cdot d_H(V_i, S_i)$$

其中 $d_H(V_i, S_i)$ 是原始 token 集合 $V_i$ 与剪枝后 token 集合 $S_i$ 之间的 Hausdorff 距离（以余弦距离为度量）。这一理论结果同时为两个模块提供了支撑：

- T-FPS 作为贪心 k-center 求解器，最小化了每个视图内的 Hausdorff 距离；
- 视图自适应优化通过为高内在重要性的视图分配更大的 token 预算（即更大的 $w_i$），直接最小化了加权误差和中的主导项。

#### 2.2 适用边界

基于论文中的实验设置和方法设计，Prune2Drive 的适用边界可归纳如下：

- **模型架构**：方法设计为 plug-and-play，理论上适用于任何使用多视图视觉 token 作为输入的 VLM 架构。论文在 DriveMM 和 DriveLMM-o1 两个模型上验证了有效性，并在 Table 3 的通用 VLM 基准（MME 等）上展示了跨任务迁移能力——保留 128 tokens（22.2% 原始量）时达到全量性能的 97.3%。
- **任务类型**：主要验证场景为自动驾驶中的视觉问答和推理任务（DriveLM、DriveLMM-o1），并在 Table 5 的 OmniDrive 视频 AD 基准上进行了扩展验证。
- **剪枝率范围**：论文在 75% 和 90% 剪枝率下进行了主要实验。极端剪枝率下的性能退化曲线需要进一步刻画。
- **计算约束**：视图自适应优化需在验证集上进行搜索（3 H100 GPU 小时），对于频繁更换模型或数据分布的场景，这一开销可能成为限制因素。

### 3. 局限性与开放问题

#### 3.1 已识别的局限性

从论文实验和分析中可提取以下局限：

- **优化成本与泛化性**：视图自适应剪枝率是在固定的验证集上搜索得到的静态分配。当测试场景的数据分布（如天气、光照、城市布局）与验证集显著不同时，预设的剪枝率可能不再最优。论文未讨论在线自适应调整机制。
- **视图间交互建模**：T-FPS 在每个视图内独立进行 token 选择，视图自适应优化仅在 token 保留率层面引入视图间协调。视图间 token 级别的交互（如跨视图冗余消除）未被利用。
- **长尾物体覆盖**：虽然 T-FPS 通过多样性保持机制在语义空间上实现了良好覆盖（Figure 1 定性展示），但对于极小目标或罕见类别的系统性保障缺乏定量分析。

#### 3.2 开放问题

- **动态剪枝策略**：当前剪枝率在推理前固定。是否存在基于输入内容动态调整剪枝率的轻量机制，以应对场景复杂度的变化？
- **与模型量化的协同**：Prune2Drive 专注于 token 级别的压缩，与模型量化、蒸馏等正交的加速技术结合后的叠加效应尚未探索。
- **实时部署验证**：论文报告了 6.40× prefill 加速和 13.4% FLOPs 降低，但未提供端到端延迟的详细分解（如 token 剪枝开销、GPU 内存占用变化），这对于实际部署评估至关重要。
- **跨传感器模态扩展**：当前方法仅处理视觉 token。在 LiDAR-视觉融合的多模态 VLM 中，T-FPS 的多样性保持原则是否可扩展到点云 token 的剪枝，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Prune2Drive_A_Plug_and_Play_Framework_for_Accelerating_Vision_Language_Models_in_Autonomous_Driving.pdf]]
