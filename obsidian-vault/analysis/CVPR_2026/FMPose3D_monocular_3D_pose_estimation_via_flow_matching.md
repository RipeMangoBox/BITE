---
title: "FMPose3D: monocular 3D pose estimation via flow matching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FMPose3D_monocular_3D_pose_estimation_via_flow_matching.pdf
project_link: null
code_link: https://github.com/AdaptiveMotorControlLab/FMPose3D
aliases:
- FMPose3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用Flow Matching替代扩散模型，学习一个由常微分方程(ODE)定义的确定性速度场，仅需少量积分步即可从噪声生成合理3D姿态；同时引入基于重投影误差的后验期望聚合模块(RPEA)，将多假设有效融合为单一鲁棒预测。
primary_logic: 将2D到3D姿态提升形式化为条件分布传输问题：以2D关节为条件，通过ODE将简单高斯分布传输到合理的3D姿态分布，每个噪声种子产生一条确定的轨迹但不同种子给出多解，最后利用近似贝叶斯后验进行加权聚合，实现高效且准确的3D姿态估计。
claims:
- FMPose3D是首个将流匹配成功应用于2D到3D姿态提升的工作；仅用3步ODE积分即达到最优精度，大幅超越扩散模型的10-50步迭代，推理速度达160 FPS以上。
- 提出的RPEA模块通过重投影误差近似后验，在Human3.6M上取得SOTA性能：N=40时MPJPE 45.5 mm，P-MPJPE 38.3 mm，显著优于DiffPose等扩散基线。
- 在动物3D姿态数据集上同样表现优异：Animal3D P-MPJPE 61.5 mm (相对AniMer下降23.5%)，CtrlAni3D 44.0 mm，证明了跨物种泛化能力。
- Human3.6M 上 MPJPE (mm) = 45.5
---

# FMPose3D: monocular 3D pose estimation via flow matching

> [!tip] 核心洞察
> 将2D到3D姿态提升形式化为条件分布传输问题：以2D关节为条件，通过ODE将简单高斯分布传输到合理的3D姿态分布，每个噪声种子产生一条确定的轨迹但不同种子给出多解，最后利用近似贝叶斯后验进行加权聚合，实现高效且准确的3D姿态估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | FMPose3D：基于流匹配的单目3D姿态估计 |
| 英文题名 | FMPose3D: monocular 3D pose estimation via flow matching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.05755) · [Code](https://github.com/AdaptiveMotorControlLab/FMPose3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FMPose3D |
| Dataset | Human3.6M, MPI-INF-3DHP, Animal3D, CtrlAni3D |

> [!tip] 效果简介
> - Human3.6M 上，MPJPE (mm) 45.5 vs 49.7 (DiffPose) (-4.2)；P-MPJPE (mm) 38.3 vs 39.2 (DiffPose) (-0.9)。
> - MPI-INF-3DHP 上，PCK (%) 86.4 (N=20) vs 84.4 (ProPose) (+2.0)；AUC (%) 54.6 (N=20) vs 52.1 (ProPose) (+2.5)。
> - Animal3D 上，P-MPJPE (mm) 61.5 vs 80.4 (AniMer) (-18.9)。

## 概要

单目3D姿态估计的核心瓶颈在于深度模糊与遮挡带来的**一对多映射**问题：同一组2D关键点可能对应多个合理的3D姿态。传统确定性回归方法只能输出单一解，而扩散模型虽能生成多样化假设，却因迭代去噪的推理机制（通常需10–50步）难以满足实时性需求。

FMPose3D 将2D到3D的姿态提升重新定义为**条件分布传输问题**：以2D关节为条件，通过常微分方程（ODE）将简单高斯分布传输到合理的3D姿态分布。其核心创新体现在两个层面：

- **生成范式替换**：采用 Flow Matching 替代扩散模型，学习确定性速度场而非随机去噪过程。每个噪声种子产生一条确定的轨迹，不同种子给出多样化解，但仅需 **3步ODE积分**即可完成推理——这使其推理速度达到 **160 FPS以上**，远超扩散基线 DiffPose 的约16 FPS。
- **多假设聚合策略**：提出基于重投影误差的后验期望聚合模块（RPEA），利用2D重投影误差作为后验概率的代理，对多假设进行关节级加权平均，将多样性转化为鲁棒的单点预测。

在方法谱系上，FMPose3D 是**首个将 Flow Matching 成功应用于2D到3D姿态提升的工作**。相较于确定性基线（如 SimpleBaseline、VideoPose3D）和概率基线（如扩散模型 DiffPose、ProPose），它在精度与效率之间取得了突破性平衡：Human3.6M 上 MPJPE 达 45.5 mm（N=40），MPI-INF-3DHP 上 PCK 达 86.4%，且在动物数据集 Animal3D 和 CtrlAni3D 上同样表现优异（P-MPJPE 61.5 mm 和 44.0 mm），展现了跨物种泛化能力。

值得注意的是，该方法仍依赖现成的2D关键点检测器，极端遮挡或罕见姿态下性能可能受限；RPEA 中的温度超参数 $\alpha$ 目前需手动设定，其自适应调整机制尚待探索。



单目3D姿态估计旨在从单张RGB图像中恢复人体或动物关节的三维坐标，是动作捕捉、人机交互、运动分析等应用的核心技术。该任务面临两个根本性瓶颈：**深度模糊**与**遮挡问题**。由于从2D图像到3D空间的映射天然存在多解性，同一组2D关键点可以对应无限多种合理的3D姿态配置，传统方法难以同时保证预测的准确性和多样性。

现有方法大致分为两类。**确定性回归方法**（如**SimpleBaseline**、**VideoPose3D**）直接将2D关键点映射为单一3D姿态，虽然推理高效，但无法刻画深度模糊带来的内在不确定性，在遮挡或罕见姿态下容易产生不可靠的估计。**概率生成方法**则试图通过建模3D姿态的条件分布来保留多解性——其中**DiffPose**等基于扩散模型的工作取得了领先的多样性表现，但其推理过程依赖随机微分方程（SDE）的迭代去噪，通常需要10–50步才能生成一个合理样本，推理速度仅约16 FPS，难以满足实时应用需求。

这种“多样性-效率”的两难困境构成了本文的核心动机：**能否设计一种生成框架，既能保持对多解性的建模能力，又能以极少的推理步数实现高速生成？**

FMPose3D的切入思路是将2D到3D姿态提升重新形式化为一个**条件分布传输问题**：以2D关节为条件，学习一个由常微分方程（ODE）定义的确定性速度场，将简单高斯分布中的样本沿着平滑轨迹“传输”到合理的3D姿态分布。这一范式变革带来两个关键优势：（1）每个噪声种子产生一条确定的轨迹，不同种子给出多样化解，保留了多解性；（2）ODE积分仅需3步即可收敛，推理速度可达160 FPS以上，较扩散模型提升近一个数量级。

此外，多假设生成后如何融合为单一鲁棒预测是另一关键问题。简单平均或逐关节选择往往无法充分利用假设间的互补信息。FMPose3D引入基于重投影误差的后验期望聚合模块（RPEA），以2D重投影误差作为近似后验的代理，对多假设进行关节级加权平均，在保持多样性的同时显著提升最终预测的精度。



## 核心方法与创新机理

FMPose3D 的核心创新可凝练为三个相互耦合的 **changed slots**，分别对应生成模型核心、多假设聚合策略和网络架构设计。三者共同构成了一条从“快速多样化采样”到“鲁棒单点输出”的完整推理链路。

### 1. 生成模型核心：从扩散SDE到流匹配ODE

单目3D姿态估计的根本瓶颈在于深度模糊与遮挡：给定同一组2D关键点，存在多个合理的3D姿态解。扩散模型（如 **DiffPose**）虽然能通过随机微分方程（SDE）的迭代去噪生成多样化的假设，但推理需10–50步反向扩散，无法满足实时需求。

FMPose3D 将2D到3D的姿态提升重新定义为**条件分布传输问题**，并采用 **Flow Matching** 替代扩散模型。其核心机制如下：

- **训练阶段**：在噪声样本 $x_0 \sim \mathcal{N}(0, I)$ 与真实3D姿态 $x_1$ 之间构建线性插值路径：
  $$x_t = (1 - t) x_0 + t x_1, \quad t \in [0, 1)$$
  目标速度场为常向量 $\nu_t = \frac{dx_t}{dt} = x_1 - x_0$。网络 $\nu_\theta$ 以2D姿态 $c$ 为条件，通过条件流匹配损失直接回归该速度：
  $$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{x_0 \sim p_0, t \sim \mathcal{U}[0,1)} \left[ \| \nu_\theta(x_t, t, c) - (x_1 - x_0) \|_2^2 \right]$$

- **推理阶段**：学到的速度场定义了一个确定性常微分方程（ODE）：
  $$\frac{dx_t}{dt} = \nu_\theta(x_t, t, c), \quad x_0 = x^{\mathrm{noise}} \sim \mathcal{N}(0, I)$$
  仅需 $S$ 步显式欧拉积分即可从噪声传输到合理3D姿态：
  $$x_{t+\frac{1}{S}} = x_t + \frac{1}{S} \nu_\theta(x_t, t, c)$$

**关键差异**：扩散模型的SDE引入随机性，需大量去噪步才能收敛；流匹配的ODE是确定性的——给定初始噪声种子，轨迹唯一确定，但不同种子产生不同解，天然支持多假设生成。实验表明，**仅需 $S=3$ 步积分即达到精度峰值**（Figure 6），推理速度达 **160.11 FPS**，而 DiffPose 在50步设置下仅 **16.36 FPS**（Table 5），速度提升近10倍。

### 2. 多假设聚合策略：RPEA后验期望近似

生成多条3D假设后，如何将其融合为单一鲁棒预测是一个非平凡问题。简单平均（Mean）忽略了假设质量的差异，每关节最佳选择（JPMA）则丢弃了其他假设中的有效信息。

FMPose3D 提出的 **RPEA（Reprojection-error-based Posterior Expectation Approximation）** 模块从贝叶斯决策论出发：最小均方误差（MMSE）估计的最优解是后验期望 $\mathbb{E}[X^{3D} | X^{2D}]$，但真实后验不可得。RPEA 的核心洞察是：**2D重投影误差可以作为后验概率的有效代理**——一个3D假设若能准确重投影回输入的2D姿态，则更可能接近真实值。

具体操作分两步：
1. **筛选**：对每个关节 $j$，计算所有 $N$ 个假设的2D重投影损失 $L_{i,j}$，保留 Top-K 个低损失候选 $\mathcal{H}_{K,j}$。
2. **加权聚合**：通过带温度参数 $\alpha$ 的 softmax 计算权重，得到关节级加权平均：
   $$\hat{X}_j^{\mathrm{RPEA}} = \sum_{H_{i,j} \in \mathcal{H}_{K,j}} w_{i,j} \cdot H_{i,j}, \quad w_{i,j} = \frac{\exp(-\alpha L_{i,j})}{\sum_{H_{k,j} \in \mathcal{H}_{K,j}} \exp(-\alpha L_{k,j})}$$

**证据强度**：Figure 3 显示，RPEA 在 MPJPE 和 P-MPJPE 两个指标上均持续优于 Mean 和 JPMA，且随着假设数量 $N$ 增加，性能单调改善——这表明 RPEA 能有效利用额外假设中的互补信息。当 $N=40$ 时，Human3.6M 上 MPJPE 达 **45.5 mm**，P-MPJPE 达 **38.3 mm**（Table 1, Table 6），显著优于 DiffPose 的 49.7 mm / 39.2 mm。

### 3. 网络架构设计：并行GCN与自注意力融合

速度预测网络 $\nu_\theta$ 需要同时捕捉人体骨架的局部拓扑约束和全局长程依赖。FMPose3D 采用**并行双分支架构**：

- **局部GCN分支**：将人体骨架视为图结构，通过图卷积捕获相邻关节（如肘-腕）的运动学关系。
- **全局自注意力分支**：通过自注意力机制建模非相邻关节（如左手-右脚）的远距离交互，这在对称动作或全身协调运动中尤为关键。

两分支特征融合后送入回归头预测速度场。消融实验（Table 4）证实：并行连接（Parallel）的 MPJPE 为 **49.3 mm**，显著优于串行 GCN→Attention 设计的 **52.5 mm**，表明局部拓扑与全局上下文需要**同时而非先后**建模，才能为速度场预测提供最丰富的表征。

### 创新耦合逻辑

三个 changed slots 并非孤立改进，而是形成了一条因果链：**ODE流匹配**提供了快速且多样化的采样能力（3步 vs. 50步），为多假设生成奠定效率基础；**并行双分支架构**确保每个假设的质量；**RPEA** 则通过重投影误差驱动的贝叶斯聚合，将多条假设的互补信息压缩为单一高精度预测。这一“快速采样-质量保证-智能融合”的闭环，是 FMPose3D 在精度和速度上同时超越扩散基线的根本原因。



FMPose3D 将单目 3D 姿态估计重新形式化为一个**条件分布传输问题**：以 2D 关键点为条件信号，通过常微分方程（ODE）将简单高斯分布传输到合理的 3D 姿态分布。其整体 pipeline 分为训练和推理两个阶段，核心由三个功能模块串联而成：**流匹配速度场建模**、**ODE 多假设生成**、以及 **RPEA 后验聚合**。

### 训练流程

训练阶段的目标是学习一个条件速度场 $\nu_\theta$，使得任意从高斯噪声到真实 3D 姿态的线性插值路径上的速度都能被准确预测。具体步骤如 Figure 1 所示：

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the training process. The process starts from a noise sample*

1. **采样噪声与目标**：从标准高斯分布采样初始噪声 $x_0 \sim \mathcal{N}(0, I)$，从训练集取真实 3D 姿态 $x_1$。
2. **构建插值路径**：在 $t \in [0,1)$ 内随机采样时间步，按线性插值 $x_t = (1-t)x_0 + t x_1$ 生成中间状态。该路径的目标速度场为常向量 $\nu_t = x_1 - x_0$。
3. **条件速度预测**：网络 $\nu_\theta$ 以当前 3D 状态 $x_t$、时间步 $t$、以及 2D 姿态条件 $c = x^{2D}$ 为输入，预测速度 $\hat{\nu}_t$。
4. **损失优化**：最小化条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{x_0 \sim p_0, t \sim \mathcal{U}[0,1)} \left[ \| \nu_\theta(x_t, t, c) - (x_1 - x_0) \|_2^2 \right]$，迫使网络在任意中间时刻都能指向正确的传输方向。

### 推理流程

推理阶段利用学到的速度场，从多个随机噪声种子出发生成多样化的 3D 姿态假设，再通过 RPEA 聚合为单一鲁棒预测（Figure 2）：

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of multi-hypothesis generation and aggregation during inference*

1. **多假设生成**：从 $M$ 个独立的高斯噪声样本 $\{x_0^{(m)}\}_{m=1}^M$ 出发，每个样本沿 ODE $\frac{dx_t}{dt} = \nu_\theta(x_t, t, c)$ 进行 $S$ 步显式欧拉积分：
   $$x_{t+\frac{1}{S}} = x_t + \frac{1}{S} \nu_\theta(x_t, t, c)$$
   积分至 $t \to 1$ 时即得到对应的 3D 姿态假设。不同噪声种子产生不同的确定性轨迹，从而覆盖多模态后验分布。
2. **RPEA 聚合**：对每个关节点 $j$，计算所有假设的 2D 重投影误差作为近似后验似然，筛选 Top-K 低误差假设，通过 softmax 加权平均得到最终关节位置：
   $$\hat{X}_j^{\mathrm{RPEA}} = \sum_{H_{i,j} \in \mathcal{H}_{K,j}} w_{i,j} \cdot H_{i,j}, \quad w_{i,j} = \frac{\exp(-\alpha L_{i,j})}{\sum_{H_{k,j} \in \mathcal{H}_{K,j}} \exp(-\alpha L_{k,j})}$$
   其中 $L_{i,j}$ 为第 $i$ 个假设在第 $j$ 个关节上的重投影损失，$\alpha$ 为温度超参数。该过程本质上是贝叶斯后验期望的近似，以重投影误差作为后验概率的代理。

### 模块关系与数据流

pipeline 内部各模块的输入输出关系如下：

| 模块 | 输入 | 输出 | 功能 |
|------|------|------|------|
| 2D 姿态嵌入编码 | 2D 关键点 $x^{2D}$ | 条件特征 $c$ | 将 2D 坐标映射为嵌入向量 |
| 3D 骨架与时间嵌入 | 当前 3D 状态 $x_t$、时间步 $t$ | 状态特征 | 编码当前姿态和时间信息 |
| 局部 GCN 分支 | 骨架图结构 + 特征 | 局部拓扑特征 | 捕获相邻关节的骨骼约束 |
| 全局自注意力分支 | 所有关节特征 | 全局上下文特征 | 建模非相邻关节的长程交互 |
| 速度预测头 | 融合后的骨干特征 | 速度向量 $\hat{\nu}_t$ | 回归当前时刻的传输速度 |
| ODE 求解器 | 噪声 $x_0$、速度场 $\nu_\theta$、条件 $c$ | 3D 姿态假设 | 通过欧拉积分生成最终姿态 |
| RPEA 聚合模块 | $M$ 个 3D 假设、2D 重投影误差 | 单一 3D 姿态 $\hat{X}^{3D}$ | 贝叶斯后验期望加权融合 |

### 关键设计选择

- **并行 GCN + 注意力架构**：消融实验（Table 4）表明，并行连接显著优于串行设计（GCN→Attention），MPJPE 从 52.5 mm 降至 49.3 mm。并行结构允许局部拓扑特征与全局上下文特征独立提取后融合，避免信息瓶颈。
- **仅需 3 步积分**：与扩散模型需要 10–50 步迭代去噪不同，FMPose3D 的确定性 ODE 仅需 $S=3$ 步欧拉积分即可达到精度峰值（Figure 6），推理速度达 160 FPS 以上，远超 DiffPose 的 16 FPS（Table 5）。
- **关节级独立聚合**：RPEA 对每个关节独立进行 Top-K 筛选和加权，允许不同关节的最优假设来自不同噪声种子，从而更灵活地利用多假设多样性。



### 3.1 流匹配：从条件分布传输到确定性速度场

FMPose3D 将单目 3D 姿态估计形式化为一个**条件分布传输问题**：以 2D 姿态为条件，学习一个由常微分方程（ODE）控制的确定性速度场，将简单高斯分布传输到合理的 3D 姿态分布。与扩散模型依赖随机微分方程（SDE）的迭代去噪不同，流匹配的 ODE 形式天然支持少步积分，推理效率显著提升。

**线性插值路径**。训练时，在噪声样本 $x_0 \sim \mathcal{N}(0, I)$ 与真实 3D 姿态 $x_1$ 之间构造线性插值：

$$x_t = (1 - t) x_0 + t x_1, \quad t \in [0, 1).$$

该路径上的**目标速度场**为常向量：

$$\nu_t = \frac{dx_t}{dt} = x_1 - x_0.$$

**条件流匹配损失**。网络 $\nu_\theta$ 以中间状态 $x_t$、时间 $t$ 和 2D 姿态条件 $c = x^{2D}$ 为输入，预测当前速度，损失函数为预测速度与目标速度的二范数误差：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{x_0 \sim p_0, t \sim \mathcal{U}[0,1)} \left[ \| \nu_\theta(x_t, t, c) - (x_1 - x_0) \|_2^2 \right].$$

**推理 ODE 与 Euler 积分**。推理时，从随机噪声 $x^{\mathrm{noise}} \sim \mathcal{N}(0, I)$ 出发，沿学到的速度场积分：

$$\frac{dx_t}{dt} = \nu_\theta(x_t, t, c), \quad x_0 = x^{\mathrm{noise}}.$$

采用显式 Euler 法离散化，设积分步数为 $S$：

$$x_{t+\frac{1}{S}} = x_t + \frac{1}{S} \nu_\theta(x_t, t, c).$$

实验表明 $S = 3$ 即可达到精度峰值（见 Figure 6），更少步数精度不足，更多步数无额外收益。这一特性使 FMPose3D 在单假设（$N=1$）下达到 160.11 FPS，远超 DiffPose 的 16.36 FPS（Table 5）。

### 3.2 RPEA：基于重投影误差的后验期望聚合

不同噪声种子 $x^{\mathrm{noise}}$ 经 ODE 积分产生不同的 3D 姿态假设，构成假设集 $\{H_i\}_{i=1}^{N}$。RPEA（Reprojection-based Posterior Expectation Aggregation）模块的目标是计算 3D 姿态的**后验期望**，将多假设融合为单一鲁棒预测。

**贝叶斯决策视角**。在最小均方误差（MMSE）准则下，最优估计为后验期望：

$$R(\hat{X}^{3D}) = \mathbb{E}\left[ \|\hat{X}^{3D} - X^{3D}\|^2 \right].$$

由于真实后验难以直接计算，RPEA 采用 **2D 重投影误差**作为后验概率的近似代理。对每个关节 $j$，计算假设 $H_i$ 的 2D 重投影损失 $L_{i,j}$，筛选 Top-K 低误差假设构成候选集 $\mathcal{H}_{K,j}$，然后进行加权聚合：

$$\hat{X}_j^{\mathrm{RPEA}} = \sum_{H_{i,j} \in \mathcal{H}_{K,j}} w_{i,j} \cdot H_{i,j},$$

其中权重通过带温度参数 $\alpha$ 的 softmax 计算：

$$w_{i,j} = \frac{\exp(-\alpha L_{i,j})}{\sum_{H_{k,j} \in \mathcal{H}_{K,j}} \exp(-\alpha L_{k,j})}.$$

**关键设计**：RPEA 以**关节级独立**方式操作——不同关节可能选择来自不同假设的候选，这比全局统一选择更灵活。消融实验（Figure 3）表明，RPEA 在增加假设数量时持续优于简单平均（Mean）和每关节最佳选择（JPMA），且同时对 MPJPE 和 P-MPJPE 保持改善。

### 3.3 网络架构：并行 GCN 与自注意力分支

速度预测网络 $\nu_\theta$ 采用双分支并行架构，分别捕获骨架的局部拓扑和全局依赖：

- **局部 GCN 分支**：将人体骨架视为图，通过图卷积捕获相邻关节的拓扑关系。
- **全局自注意力分支**：建模非相邻关节间的长程交互，如左右手协调、四肢与躯干的关联。
- **嵌入层**：2D 姿态经 2D 骨架嵌入层编码为特征；当前 3D 状态和时间 $t$ 分别经 3D 骨架嵌入层和时间嵌入层编码。
- **速度预测头**：将融合后的骨干特征映射为预测速度。

消融实验（Table 4）证实：并行连接（Parallel）的 MPJPE 为 49.3 mm，显著优于串行连接（GCN→Attn）的 52.5 mm，验证了同时保留局部拓扑与全局上下文对速度场建模的必要性。



## 实验与关键发现

### 核心定量结果

FMPose3D在人体和动物3D姿态估计的多个基准上取得最优性能，以仅3步ODE积分的极简推理配置超越需要10-50步迭代的扩散模型基线。

**Human3.6M（室内人体基准）**：在检测2D姿态输入下，FMPose3D以N=40个假设取得平均MPJPE 45.5 mm，显著优于DiffPose的49.7 mm（-4.2 mm，-8.4%）。在P-MPJPE（Procrustes对齐后）指标上，同样以38.3 mm领先于DiffPose的39.2 mm。即便仅使用N=2个假设，FMPose3D的MPJPE已达47.3 mm，已超过多数先前方法的大量假设配置。完整对比见Table 1和Table 6。

**MPI-INF-3DHP（多场景人体基准）**：该数据集包含GS（绿幕）、noGS（非绿幕）和Outdoor（室外）三个场景。FMPose3D在所有场景上均取得最优：N=20时全场景PCK 86.4%（vs ProPose 84.4%，+2.0个百分点），AUC 54.6%（vs ProPose 52.1%，+2.5个百分点）。值得注意的是，FMPose3D在室外场景（Outdoor）的PCK达82.2%，较ProPose的78.5%提升显著，表明方法对野外场景的鲁棒性。

**动物3D姿态估计**：在Animal3D数据集上，FMPose3D的P-MPJPE为61.5 mm，相比基于SMAL模型拟合的AniMer（80.4 mm）下降23.5%，证明了跨物种泛化的有效性。在CtrlAni3D上，P-MPJPE为44.0 mm，与AniMer的44.1 mm持平，但FMPose3D无需任何动物先验模型，方法更通用。

**3DPW（野外人体基准）**：在零样本评估设置下（仅在Human3.6M训练），FMPose3D的MPJPE为78.0 mm，PA-MPJPE为51.8 mm，展现了良好的域外泛化能力（Table 7）。

### 消融实验与机制分析

#### 1. 并行GCN+注意力架构优于串行设计

Table 4的消融实验对比了不同的网络架构设计。仅使用GCN分支时MPJPE为53.8 mm，仅使用自注意力分支时为52.5 mm。将两者串行连接（GCN→Attention）反而使性能退化至52.5 mm。而**并行连接并融合**两个分支的设计将MPJPE降至49.3 mm（N=1时），验证了局部拓扑建模与全局依赖捕获的互补性——GCN捕获骨架相邻关节的显式连接关系，自注意力建模非相邻关节间的长程交互，二者并行处理避免了串行带来的信息瓶颈。

#### 2. RPEA聚合策略的贝叶斯合理性

Figure 3对比了三种多假设聚合策略随假设数量N增加的性能变化：

- **简单平均（Mean）**：MPJPE随N增加缓慢下降，但N>10后趋于饱和，因为低质量假设的等权贡献稀释了高质量假设。
- **每关节最佳选择（JPMA）**：直接选择每个关节的重投影误差最低的假设，虽然利用了误差信号，但由于各关节可能来自不同假设，破坏了3D姿态的结构一致性，P-MPJPE表现不佳。
- **RPEA**：基于重投影误差的后验期望近似，在N=40时MPJPE降至45.5 mm，P-MPJPE降至38.3 mm，且两条曲线均未饱和，表明RPEA能持续从更多假设中获益。其核心机制是：对每个关节独立计算重投影误差$L_{i,j}$，筛选Top-K低误差假设，通过softmax加权聚合，权重为$w_{i,j} \propto \exp(-\alpha L_{i,j})$。这种关节级后验近似既利用了2D观测的似然信息，又保持了各关节估计的独立性。

#### 3. 仅需3步ODE积分即可收敛

Figure 6展示了积分步数S对精度的影响。当S=1时MPJPE较高（约52 mm），因为单步欧拉积分无法充分逼近连续ODE轨迹。S增至3时，MPJPE和P-MPJPE均达到最优平台（S∈{3,4,5}）。进一步增加S至20以上，精度不再提升甚至微幅波动，说明3步已足够捕获速度场的几何结构。这一性质直接源于Flow Matching的确定性ODE特性——与扩散模型的随机微分方程（SDE）需要多步去噪不同，ODE轨迹是光滑的，少量离散化步即可高精度求解。

#### 4. 推理速度：160 FPS vs 扩散模型的16 FPS

Table 5的推理速度对比揭示了Flow Matching的核心效率优势。在单张RTX 4090 GPU上：

- FMPose3D（N=1，S=3）：160.11 FPS
- DiffPose（N=1，50步）：16.36 FPS
- FMPose3D（N=40，S=3）：4.63 FPS（需生成40条独立ODE轨迹）

速度差距约10倍，根因在于：扩散模型需要50步逐步去噪，每步都需完整前向传播；而FMPose3D仅需3步ODE积分。当需要多假设时，各假设可完全并行生成，实际延迟增长可控。

#### 5. 训练数据效率

Table 8显示，在Human3.6M上仅使用10%训练数据（约312k帧），FMPose3D的P-MPJPE已达43.5 mm；使用80%数据时降至39.3 mm，接近全量数据的38.3 mm。在动物数据集上，由于总样本量小（Animal3D仅3k帧），10%数据时性能波动较大（标准差±2.3 mm），但80%数据时已稳定。这表明Flow Matching的分布传输范式具有较好的样本效率，但极小数据集上仍需谨慎。

#### 6. 不确定性估计的可靠性

Figure 8分析了各关节的多假设标准差（不确定性）与实际MPJPE误差的相关性。结果表明，不确定性高的关节（如手腕、脚踝等末端关节）确实对应更高的实际误差，验证了模型输出的多假设分布能够有效表征认知不确定性。Figure 9的可视化案例进一步显示，在遮挡或深度模糊场景下，模型在受影响的关节（左肘、左腕）上产生更高的假设方差，为下游应用提供了可信的不确定性信号。

### 失败模式与局限性

尽管FMPose3D在多个基准上表现优异，仍存在以下局限：

1. **2D检测器依赖**：方法以检测的2D姿态为输入条件，当2D关键点存在较大检测误差（如严重遮挡、运动模糊）时，3D预测质量会随之下降。这是所有2D-to-3D提升方法的共性瓶颈，非FMPose3D特有。

2. **极端姿态与罕见视角**：模型主要在Human3.6M的室内受控场景训练，对于3DPW中出现的倒地、自遮挡严重等极端姿态，零样本性能虽优于多数方法，但仍存在明显误差。

3. **RPEA的超参数敏感性**：温度参数α控制重投影误差到权重的映射锐度，当前固定为经验值。在2D检测噪声较大时，过大的α可能导致过度信任不准确的2D观测，需要手动验证最优设置。

4. **动物数据集的样本限制**：Animal3D仅含约3k帧训练数据，FMPose3D在该数据集上虽大幅超越AniMer，但绝对P-MPJPE（61.5 mm）仍显著高于人体基准，部分源于训练数据不足导致的分布覆盖不完整。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with the state-of-the-art methods on Human3.6M under MPJPE. The detected 2D pose is used as input. ?? denotes the number of hypotheses. Red: Best. Blue: Second Best. Grey : our method*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparisons with state-of-the-art methods on MPI-INF-3DHP*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/005_Table_3.jpg]]
*Table 3: Quantitative comparisons with state-of-the-art methods on Animal3D and CtrlAni3D*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/006_Table_4.jpg]]
*Table 4: Ablation study on different model designs. Serial: GCN followed by Attention (GCN→Attn). Parallel: GCN and Attention are computed in two branches and fused*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/007_Table_5.jpg]]
*Table 5: Inference speed. Frames per second (FPS) were measured on a single GeForce RTX 4090 GPU. ?? denotes the number of hypothesis. For DiffPose [16], we follow the setting in the original paper with 50 reverse diffusion steps at inference*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/008_Figure_3.jpg]]
*Figure 3: Comparison of different aggregation strategies on the Human3.6M test set. The top plot reports MPJPE, while the bottom plot shows P-MPJPE*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparison of DiffPose [16] and FMPose3D on Human3.6M. The blue pose represents the predicted results, while the red pose represents the ground truth*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/011_Figure_6.jpg]]
*Figure 6: Effect of the number of integration steps ?? on inference accuracy. The blue curve shows MPJPE (read from the left vertical axis), and the orange curve shows P-MPJPE (read from the right vertical axis); the shaded region marks the range*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/012_Table_6.jpg]]
*Table 6: Quantitative comparison with the state-of-the-art methods on Human3.6M under P-MPJPE. The detected 2D pose is used as input. ?? denotes the number of hypotheses. Red: Best. Blue: Second Best. Grey : our method*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2602_05755/figures/015_Table_7.jpg]]
*Table 7: Results on 3DPW. Top: methods trained on 3DPW. Bottom: methods without 3DPW training (zero-shot evaluation)*



## 定位与知识库关联

### 1. 问题域与核心瓶颈

单目3D姿态估计长期受困于**深度模糊**与**遮挡**两大固有问题：给定一个2D关键点输入，理论上存在无穷多个合理的3D解。传统方法将这一问题建模为确定性回归（如 **SimpleBaseline**、**VideoPose3D**），虽能快速推理，但只能输出单一预测，无法表达多解性，在遮挡场景下鲁棒性不足。

近期扩散模型（如 **DiffPose**）通过将2D-3D提升建模为条件生成过程，引入了多假设能力，显著提升了多样性和鲁棒性。然而，扩散模型基于随机微分方程（SDE）的迭代去噪机制导致推理需10-50步，速度难以满足实时需求。**ProPose** 等后续工作在此基础上进一步改进，但仍未根本解决效率瓶颈。

FMPose3D 的工作正是在这一矛盾点上切入：**如何在保持多假设生成能力的同时，实现接近确定性方法的推理速度？**

### 2. 方法谱系定位

FMPose3D 的方法学定位可以沿两个维度展开：

**生成模型维度：从SDE到ODE的范式转移**

| 方法 | 生成范式 | 推理机制 | 推理步数 | 速度（FPS） |
|------|----------|----------|----------|-------------|
| SimpleBaseline | 确定性回归 | 单次前向 | 1 | 极高 |
| DiffPose | 扩散模型（SDE） | 迭代去噪 | ~50 | ~16 |
| ProPose | 扩散/概率混合 | 迭代 | 多步 | 中等 |
| **FMPose3D** | **流匹配（ODE）** | **确定性积分** | **3** | **~160** |

FMPose3D 是**首个将 Flow Matching 成功应用于2D-3D姿态提升的工作**。其核心创新在于将姿态估计形式化为条件分布传输问题：以2D关节为条件，通过一个由常微分方程（ODE）定义的确定性速度场，将简单高斯分布传输到合理的3D姿态分布。与扩散模型的SDE不同，ODE路径是确定性的——给定相同噪声种子和条件，生成结果唯一；但不同种子产生不同轨迹，天然支持多假设生成。

这一设计带来了根本性的效率优势：流匹配仅需3步显式欧拉积分即可达到精度峰值，而扩散模型需要数十步。在 GeForce RTX 4090 上，FMPose3D 单假设推理达 **160.11 FPS**，远超 DiffPose 的 **16.36 FPS**，将生成式3D姿态估计首次推入实时域。

**聚合策略维度：从简单融合到贝叶斯后验近似**

多假设生成后如何聚合为单一预测，是概率方法的另一关键设计点。早期工作采用简单平均或每关节最佳选择（JPMA），未能充分利用假设间的质量差异。

FMPose3D 提出的 **RPEA（Reprojection-error-based Posterior Expectation Approximation）** 模块，基于贝叶斯决策理论中的后验期望最小化均方误差风险的原理，以2D重投影误差作为后验概率的代理，对每个关节独立进行Top-K筛选和加权平均：

$$\hat{X}_j^{\mathrm{RPEA}} = \sum_{H_{i,j} \in \mathcal{H}_{K,j}} w_{i,j} \cdot H_{i,j}, \quad w_{i,j} = \frac{\exp(-\alpha L_{i,j})}{\sum_{H_{k,j} \in \mathcal{H}_{K,j}} \exp(-\alpha L_{k,j})}$$

这一设计无需额外网络模块，计算代价极低，却能在假设数量增加时持续提升精度，显著优于简单平均和JPMA策略。

### 3. 网络架构的谱系继承与改进

FMPose3D 的速度预测网络采用了**并行GCN+自注意力**的双分支设计，这一架构选择源于对现有工作的消融验证：

- **GCN分支**：继承自基于图卷积的姿态估计方法，捕获骨架相邻关节的局部拓扑关系
- **自注意力分支**：借鉴Transformer类方法的全局建模能力，处理非相邻关节间的长程交互
- **并行融合**：消融实验表明，并行连接（MPJPE 49.3 mm）显著优于串行设计（GCN→Attention, MPJPE 52.5 mm），说明局部拓扑和全局依赖应同时而非顺序提取

### 4. 跨域泛化边界

FMPose3D 在以下数据集上验证了其泛化能力：

- **Human3.6M**（室内受控）：MPJPE 45.5 mm（N=40），P-MPJPE 38.3 mm，均为SOTA
- **MPI-INF-3DHP**（室内+室外混合）：PCK 86.4%，AUC 54.6%（N=20），超越ProPose
- **3DPW**（野外场景）：零样本评估显示合理性能，证明室内训练的模型具有一定野外泛化能力
- **Animal3D / CtrlAni3D**（跨物种）：P-MPJPE 61.5 mm / 44.0 mm，相对AniMer分别下降23.5%和0.2%，表明方法对非人体骨架同样有效

值得注意的是，动物数据集上FMPose3D未使用水平翻转增强（动物姿态不具备人体对称性），仍取得优异结果，验证了方法本身的泛化能力而非数据增强的贡献。

### 5. 适用边界与局限

1. **2D检测器依赖**：方法以现成2D关键点检测器（如CPN）的输出为输入，当2D检测出现较大偏差或关键点缺失时，3D预测质量会随之下降。这是整个2D-3D提升范式的共有局限。

2. **极端遮挡与罕见姿态**：模型主要在Human3.6M的室内受控场景上训练，虽然3DPW零样本评估展示了野外泛化潜力，但在极端遮挡、罕见视角或大幅度运动模糊场景下的性能缺乏充分验证。

3. **时序信息缺失**：当前设计仅处理单帧输入，未利用视频帧间的时序一致性。在快速运动或短暂完全遮挡的场景中，时序信息可能对维持追踪连续性至关重要。

4. **训练数据效率**：尽管10%训练数据下Human3.6M的P-MPJPE仍为43.5 mm，但在极小样本场景（如Animal3D仅3k训练帧）下，性能提升空间仍较大，半监督或自监督扩展值得探索。

### 6. 开放问题

1. **RPEA温度参数的自适应**：当前α为全局超参数，能否根据各关节的不确定性（由多假设的标准差估计）自适应调整，以在高低不确定性区域采用不同的聚合策略？

2. **时序扩展**：如何自然地将流匹配框架扩展到视频输入？可能的路径包括在条件c中引入时序特征，或设计时序一致的速度场。

3. **多任务损失融合**：流匹配的速度场能否直接与骨骼长度一致性、关节角度约束等物理先验结合，在不增加积分步数的前提下提升合理性？

4. **与检测器联合优化**：当前2D检测器与3D提升模块独立训练，端到端联合优化或使用检测器不确定性作为额外条件信号，可能进一步提升鲁棒性。

5. **更高效的ODE求解器**：当前使用显式欧拉法，更高阶的求解器（如RK4）或自适应步长策略能否在保持速度优势的同时进一步提升精度？



## 原文 PDF

![[paperPDFs/CVPR_2026/FMPose3D_monocular_3D_pose_estimation_via_flow_matching.pdf]]
