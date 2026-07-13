---
title: "MAGICIAN: Efficient Long-Term Planning with Imagined Gaussians for Active Mapping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MAGICIAN_Efficient_Long_Term_Planning_with_Imagined_Gaussians_for_Active_Mapping.pdf
project_link: "https://shiyao-li.github.io/magician/"
code_link: null
aliases:
- MAGICIAN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用预训练神经占用网络先验预测未知区域的占用概率，通过将覆盖增益计算重构为体积渲染过程，并使用3D高斯泼溅（Imagined Gaussians）实现快速前馈渲染评估（每次约0.002秒），从而允许在束搜索中高效优化长期轨迹的累积覆盖增益。
primary_logic: 揭示表面覆盖增益积分与体积渲染方程的结构等价性，将占用概率作为高斯透明度、新颖性作为颜色，通过GPU加速的光栅化渲染实现每像素覆盖增益的即时估算，计算速度提升25倍，使长期树搜索规划变得可行。
claims:
- MAGICIAN在Macarons++数据集上最终覆盖率达到0.919，超过贪心方法MACARONS的0.819，绝对提升10个百分点，相对提升12.2%。
- Imagined Gaussians将覆盖增益计算速度从MACARONS的蒙特卡洛方法的0.05秒提高到0.002秒，实现25倍加速。
- 增加束搜索宽度和前瞻步数能稳定提升性能，AUC绝对提升6.3%，最终覆盖率绝对提升9.3%。
- Macarons++ 上 AUC = 0.721
---

# MAGICIAN: Efficient Long-Term Planning with Imagined Gaussians for Active Mapping

> [!tip] 核心洞察
> 揭示表面覆盖增益积分与体积渲染方程的结构等价性，将占用概率作为高斯透明度、新颖性作为颜色，通过GPU加速的光栅化渲染实现每像素覆盖增益的即时估算，计算速度提升25倍，使长期树搜索规划变得可行。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAGICIAN: 基于想象高斯的主动建图高效长期规划 |
| 英文题名 | MAGICIAN: Efficient Long-Term Planning with Imagined Gaussians for Active Mapping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22650) · [Project](https://shiyao-li.github.io/magician/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MAGICIAN |
| Dataset | Macarons++, Matterport3D |

> [!tip] 效果简介
> - Macarons++ 上，AUC 0.721 vs 0.647 (MACARONS) (+0.074)；Final Coverage 0.919 vs 0.819 (MACARONS) (+0.100)。
> - Matterport3D (Wheeled Robot) 上，Comp. (%) 85.45 vs 79.38 (NBP ) (+6.07)。
> - Matterport3D (Drone) 上，Comp. (%) 96.83 vs 95.32 (ActiveGamer ) (+1.51)。

## 概要

主动建图任务要求智能体自主规划观测轨迹，以最少步数实现对未知场景的完整三维覆盖。现有方法普遍采用**贪心次最佳视角（Next-Best-View, NBV）选择**策略，每步仅优化当前视野的即时覆盖增益，缺乏对长期轨迹的全局推理能力，导致探索效率低下和重复路径。更深层的瓶颈在于：表面覆盖增益的传统计算依赖蒙特卡洛积分，单次评估耗时约0.05秒，无法高效评估大量候选轨迹，从而将规划限制在短视的贪心框架内。

MAGICIAN针对上述瓶颈提出了两个核心突破：

1. **覆盖增益的体积渲染重构**：揭示表面覆盖增益积分与体积渲染方程的结构等价性——将占用概率映射为高斯透明度、新颖性映射为颜色，通过GPU加速的光栅化渲染实现每像素覆盖增益的即时估算，计算速度从0.05秒降至0.002秒（**25倍加速**），使长期树搜索规划在计算上变得可行。

2. **基于束搜索的长期轨迹优化**：利用预训练神经占用网络提供的结构先验，将未知区域几何预测为**Imagined Gaussians**（想象高斯），在束搜索框架中增量评估候选轨迹的累积覆盖增益，选择多步累积收益最大的轨迹执行，从而突破贪心单步优化的局限。

在Macarons++基准上，MAGICIAN的最终覆盖率达到0.919，相较贪心方法MACARONS的0.819**绝对提升10个百分点**（相对提升12.2%）；AUC从0.647提升至0.721。在Matterport3D数据集上，该方法在轮式机器人和无人机两种设置下均取得最优，覆盖率分别达到85.45%和96.83%。消融实验表明，增大束搜索宽度和前瞻步数可带来AUC 6.3%、最终覆盖率9.3%的绝对提升，验证了长期规划的有效性。

主动三维建图（Active 3D Mapping）要求自主机器人通过主动选择观测视角，在未知环境中高效、完整地重建场景表面。该任务的核心挑战在于：机器人必须在有限的步数预算内，从海量候选视角中规划出一条最大化表面覆盖的探索轨迹。近年来，基于学习的主动建图方法（如**MACARONS**、**SCONE**、**ActiveGamer**等）在单步视角选择上取得了显著进展，但其规划策略普遍存在一个根本性瓶颈——**缺乏长期规划能力**。

### 现有方法的缺口：贪心策略与计算瓶颈

当前主流的主动建图方法大多采用**贪心次最佳视角（NBV）选择**策略。在每一步，机器人仅评估当前可达的候选位姿，选择覆盖增益最大的视角执行，然后基于新观测更新场景模型并重复该过程。这种短视策略带来两个严重后果：

1. **探索效率低下**：贪心策略无法预见未来的观测收益，容易将机器人引导至局部信息丰富的区域，而忽略全局未探索空间，导致大量重复路径和覆盖盲区。
2. **重复路径浪费步数**：缺乏对长期轨迹的整体优化，机器人可能在已探索区域反复穿行，消耗宝贵的步数预算。

更关键的是，**长期规划在技术上长期难以实现**，其核心障碍在于覆盖增益的计算效率。现有方法（如MACARONS）采用蒙特卡洛积分，通过对占用网络和新颖性网络进行大量采样来估算候选视角的表面覆盖增益。这一过程每次约需**0.05秒**——当规划范围扩展至多步轨迹时，需评估的候选视角数量呈指数级增长，蒙特卡洛积分的计算开销使长期树搜索规划在实时系统中变得不可行。

### 核心洞察：覆盖增益与体积渲染的结构等价性

MAGICIAN的提出源于一个关键的数学洞察：**表面覆盖增益的积分公式与体积渲染方程具有完全相同的结构**。具体而言，覆盖增益衡量的是候选视角视锥内、尚未被观测的真实表面面积：

$$
G(\mathbf{c}) = \int_{\partial \mathcal{E} \cap \mathrm{VF}(\mathbf{c})} \sigma(\mathbf{x}) \cdot o(\mathbf{x}, \mathbf{c}) \cdot \gamma(\mathbf{x}|\mathbf{C}_t) d\mathbf{x}
$$

其中 $\sigma$ 为表面指示函数，$o$ 为遮挡函数，$\gamma$ 为新颖性函数。该积分可被重构为沿光线的体积渲染过程——将占用概率视为密度场、新颖性视为颜色场，通过GPU加速的光栅化渲染实现每像素覆盖增益的即时估算。

基于这一洞察，MAGICIAN提出了**Imagined Gaussians**：一种从预训练神经占用网络采样的3D高斯泼溅表示。高斯的透明度编码占用概率，颜色编码新颖性，使得覆盖增益计算从昂贵的蒙特卡洛采样转化为高效的体积渲染，计算速度从**0.05秒降至0.002秒，实现25倍加速**。这一效率突破首次使长期束搜索规划成为现实——机器人可以在每个决策点评估多条候选轨迹的累积覆盖增益，从而选择全局更优的探索路径。

### 本文动机

综上，MAGICIAN旨在解决主动建图中的两个核心问题：**如何克服贪心规划的短视性**，以及**如何使长期规划的计算开销可控**。通过将覆盖增益计算重构为体积渲染、并利用3D高斯泼溅实现前馈加速，该方法在保持实时性的同时，显著提升了探索效率和最终建图完整性。

## 核心方法与创新机理

MAGICIAN 的核心创新在于将主动建图从**贪心单步视角选择**推进到**长期轨迹优化**，并通过**覆盖增益计算与体积渲染的结构等价性**实现高效评估。具体而言，该方法在三个关键维度上改变了传统范式：

### 1. 规划策略：从贪心到长期束搜索

现有方法（如 **SCONE**、**MACARONS**）采用贪心策略，每次仅选择当前覆盖增益最大的下一个最佳视角（NBV）。这种短视行为导致探索效率低、重复路径多。MAGICIAN 首次将规划目标重新定义为**最大化长期轨迹的累积覆盖增益**：

$$G(\tau) = \sum_{i=1}^{N_d} G(\mathbf{c}_{t+i})$$

其中 $\tau$ 为长度为 $N_d$ 的候选轨迹，$G(\mathbf{c}_{t+i})$ 为每一步的覆盖增益。通过束搜索（beam search）在离散动作空间中增量构建候选轨迹，每步保留覆盖增益最高的 $N_b$ 条候选，最终选择累积增益最大的轨迹执行。这一设计使机器人能够前瞻性地规划路径，避免进入覆盖增益低或重复探索的区域。

### 2. 覆盖增益估算：从蒙特卡洛积分到体积渲染

这是 MAGICIAN 最关键的洞察。传统方法（如 MACARONS）通过蒙特卡洛采样对占用网络和新颖性网络进行积分来估算覆盖增益，每次计算约需 **0.05 秒**，无法支持大量候选轨迹的实时评估。MAGICIAN 揭示了**表面覆盖增益积分与体积渲染方程的结构等价性**：

$$G(\mathbf{c}) = \int_{\partial \mathcal{E} \cap \mathrm{VF}(\mathbf{c})} \sigma(\mathbf{x}) \cdot o(\mathbf{x}, \mathbf{c}) \cdot \gamma(\mathbf{x}|\mathbf{C}_t) d\mathbf{x}$$

通过将占用概率 $\hat{\sigma}$ 映射为体积密度、新颖性 $\hat{\gamma}$ 映射为颜色、遮挡关系通过透过率近似，上述积分可重写为体积渲染形式：

$$I(\mathbf{p}) = \int_0^{+\infty} \hat{\sigma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) \cdot \hat{o}(\mathbf{o}+s\mathbf{d}, \mathbf{c}) \cdot \hat{\gamma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) ds$$

最终覆盖增益通过对所有有效像素的渲染新颖性进行深度加权求和得到：

$$G_{\mathrm{rendered}}(\mathbf{c}) = \sum_{\mathbf{p} \in \mathcal{P}_{\mathrm{valid}}} w_{\mathrm{depth}}(\mathbf{p}) I_{\mathrm{novelty}}(\mathbf{p})$$

其中深度加权因子 $w_{\mathrm{depth}}(\mathbf{p}) = \min\left(1, \left(\frac{D(\mathbf{p})}{D_{\mathrm{th}}}\right)^2\right)$ 防止近距离过度采样导致增益虚高。

### 3. 场景表征：Imagined Gaussians

为实现上述体积渲染的高效计算，MAGICIAN 提出了 **Imagined Gaussians**——一种从预训练神经占用网络导出的 3D 高斯泼溅表征。其核心设计在于：**高斯透明度编码占用概率**（预测该点存在表面的可能性），**颜色编码二值新颖性**（该点是否已被观测）。这一表征使覆盖增益估算可直接利用 GPU 加速的光栅化渲染管线，将单次计算时间从 0.05 秒降至 **0.002 秒，实现 25 倍加速**。

Imagined Gaussians 的另一个关键特性是**状态独立性**：在束搜索过程中，每条候选轨迹维护独立的 Imagined Gaussian 新颖性状态，通过渲染深度图更新已观测区域的新颖性标记，确保不同候选轨迹之间的评估相互隔离且可并行。

### 创新有效性验证

消融实验直接验证了上述创新的贡献：
- **体积渲染 vs 蒙特卡洛**：即使仅用于贪心 NBV（束宽=前行步数=1），Imagined Gaussians 的 AUC 仍比 MACARONS 高 **5.2%**，最终覆盖率高 **10.9%**，表明体积渲染方法本身优于蒙特卡洛近似。
- **长期规划 vs 贪心**：将束搜索宽度从 1 增至 10、前瞻步数从 1 增至 10 时，AUC 提升 **6.3%**，最终覆盖率提升 **9.3%**，验证了长期规划的有效性。
- **计算效率**：25 倍加速（0.002 秒 vs 0.05 秒）使束搜索在计算上可行，是长期规划得以实现的基础。

MAGICIAN 是一个面向主动三维建图的长期轨迹规划框架，其核心设计围绕一个关键瓶颈展开：**现有方法采用贪心单步次最佳视角选择，缺乏对长期累积覆盖增益的建模能力，导致探索效率低、重复路径多；同时，传统基于蒙特卡洛采样的覆盖增益估算速度过慢（每次约 0.05 秒），无法支撑大量候选轨迹的实时评估。**

针对这一瓶颈，MAGICIAN 引入了一个因果调控变量——**利用预训练神经占用网络的先验来预测未知区域的几何结构，并将覆盖增益计算重构为体积渲染过程**，从而通过 3D 高斯泼溅（Imagined Gaussians）实现快速前馈渲染评估（每次约 0.002 秒），使得在束搜索中高效优化长期轨迹的累积覆盖增益成为可能。

### 框架总览

MAGICIAN 的整体 pipeline 由三个核心模块串联构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MAGICIAN framework. At time t, we first predict the occupancy field using the occupancy model and update the Imagined Gaussians. We can then efficiently estimate the coverage gain and apply beam search to plan*

1. **神经占用预测模型**：在时刻 $t$，基于已观测的深度数据，通过一个基于 Transformer 的占用网络预测整个场景的占用概率场 $\hat{\sigma}(\mathbf{x}|\mathbf{C}_t)$。该模型在 ShapeNet 上预训练、在三维场景上微调，为后续的 Imagined Gaussians 提供结构先验。
2. **Imagined Gaussians 生成与渲染**：将占用场转化为一组 3D 高斯——高斯透明度编码占用概率，颜色编码新颖性（即该区域是否已被观测）。对于任意候选相机位姿 $\mathbf{c}$，通过体积渲染生成新颖性图，再对所有像素求和得到该位姿的覆盖增益 $G(\mathbf{c})$。
3. **束搜索规划器**：以当前 Imagined Gaussians 的状态为起点，增量扩展 $N_b$ 条候选轨迹，每条轨迹前瞻 $N_d$ 步。每步扩展时，独立更新各束的高斯新颖性状态，计算累积覆盖增益 $G(\tau) = \sum_{i=1}^{N_d} G(\mathbf{c}_{t+i})$，最终选择累积增益最高的轨迹执行前 $N_f$ 步，随后闭环重规划。

### 核心洞察：覆盖增益与体积渲染的结构等价性

MAGICIAN 的关键理论洞察在于揭示了表面覆盖增益积分与体积渲染方程之间的结构等价性。传统的覆盖增益定义在真实表面 $\partial\mathcal{E}$ 与视锥 $\mathrm{VF}(\mathbf{c})$ 的交集上进行积分：

$$G(\mathbf{c}) = \int_{\partial \mathcal{E} \cap \mathrm{VF}(\mathbf{c})} \sigma(\mathbf{x}) \cdot o(\mathbf{x}, \mathbf{c}) \cdot \gamma(\mathbf{x}|\mathbf{C}_t) d\mathbf{x}$$

通过将表面积分松弛为沿光线的体积积分，并用占用概率 $\hat{\sigma}$ 替代真实表面指示函数、用渲染透过率 $T(s)$ 近似遮挡项，可将覆盖增益重写为体积渲染形式：

$$I(\mathbf{p}) = \int_0^{+\infty} \hat{\sigma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) \cdot \hat{o}(\mathbf{o}+s\mathbf{d}, \mathbf{c}) \cdot \hat{\gamma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) ds$$

这一重构使得覆盖增益可以直接通过 GPU 加速的 3D 高斯光栅化渲染器计算——对每个像素 $\mathbf{p}$ 渲染其新颖性 $I_{\mathrm{novelty}}(\mathbf{p})$，再经深度加权求和得到最终增益：

$$G_{\mathrm{rendered}}(\mathbf{c}) = \sum_{\mathbf{p} \in \mathcal{P}_{\mathrm{valid}}} w_{\mathrm{depth}}(\mathbf{p}) I_{\mathrm{novelty}}(\mathbf{p})$$

其中深度加权因子 $w_{\mathrm{depth}}(\mathbf{p}) = \min\left(1, \left(\frac{D(\mathbf{p})}{D_{\mathrm{th}}}\right)^2\right)$ 用于防止近距离区域过度采样导致增益虚高。

### 数据流与闭环机制

MAGICIAN 的完整数据流如下：RGB-D 观测 → 占用模型预测占用场 → 生成/更新 Imagined Gaussians → 束搜索评估候选轨迹的累积覆盖增益 → 执行最优轨迹的前 $N_f$ 步 → 收集新观测 → 闭环重规划。这一闭环机制使得方法能够逐步修正探索初期的几何预测误差，如 Figure 4 所示，Imagined Gaussians 随着探索推进逐渐与真实网格对齐。

### 计算效率瓶颈的突破

Imagined Gaussians 带来的计算加速是使长期规划可行的关键。将覆盖增益估算从蒙特卡洛采样（MACARONS 方法，每次约 0.05 秒）转变为体积渲染（每次约 0.002 秒），实现了 **25 倍加速**。这一量级的效率提升使得束搜索能够在合理时间内评估大量候选轨迹（$N_b=10$，$N_d=10$ 时需评估数百个候选位姿），从而将规划视野从单步贪心扩展到多步前瞻优化。

MAGICIAN 的核心方法论围绕三个紧密耦合的模块展开：**神经占用预测模型**提供场景几何先验，**Imagined Gaussians 生成与渲染**实现高效覆盖增益估算，**束搜索规划器**利用前两个模块在长期轨迹空间中进行优化搜索。以下逐一剖析各模块的设计逻辑与关键公式。

### 神经占用预测模型

该模块的职责是在探索过程中持续预测整个场景的占用概率场，为后续的覆盖增益计算提供几何先验。模型架构遵循先前工作的多层 Transformer 设计，先在 ShapeNet 上预训练，再在三维场景数据上微调。其输入为当前已观测到的点云和对应的相机位姿，输出为空间中任意点的占用概率 $\hat{\sigma}(\mathbf{x}|\mathbf{C}_t)$，表示在已知历史观测 $\mathbf{C}_t$ 的条件下点 $\mathbf{x}$ 被表面占据的置信度。

这一预测能力是长期规划的关键——即使在尚未观测的区域，模型也能基于已看到的局部结构推断出合理的几何假设，从而避免盲目探索。Figure 4 展示了随着探索推进，Imagined Gaussians 逐渐与真实网格对齐的演化过程，验证了占用预测的可靠性。

### 表面覆盖增益的形式化

主动建图的核心目标是最大化新揭示的表面面积。给定候选相机位姿 $\mathbf{c}$，其表面覆盖增益定义为：

$$G(\mathbf{c}) = \int_{\partial \mathcal{E} \cap \mathrm{VF}(\mathbf{c})} \sigma(\mathbf{x}) \cdot o(\mathbf{x}, \mathbf{c}) \cdot \gamma(\mathbf{x}|\mathbf{C}_t) d\mathbf{x}$$

其中各变量含义如下：
- $\partial \mathcal{E}$：场景的真实表面；
- $\mathrm{VF}(\mathbf{c})$：相机位姿 $\mathbf{c}$ 的视锥体；
- $\sigma(\mathbf{x})$：点 $\mathbf{x}$ 是否位于真实表面上的指示函数；
- $o(\mathbf{x}, \mathbf{c})$：点 $\mathbf{x}$ 从位姿 $\mathbf{c}$ 是否可见（未被遮挡）；
- $\gamma(\mathbf{x}|\mathbf{C}_t)$：点 $\mathbf{x}$ 相对于历史观测 $\mathbf{C}_t$ 的新颖性，即该表面区域此前是否未被充分观测。

该积分的直观含义是：在候选视角的视锥与真实表面的交集上，对“可见且新颖”的表面区域进行累积。然而，直接计算这一积分需要已知真实表面 $\partial \mathcal{E}$，且通常依赖蒙特卡洛采样，计算代价高昂。

### 覆盖增益的体积渲染重构

MAGICIAN 的核心洞察在于揭示覆盖增益积分与体积渲染方程的结构等价性。通过对真实表面积分进行松弛，将表面约束替换为占用概率的密度场，覆盖增益可近似为体积渲染形式：

$$I(\mathbf{p}) = \int_0^{+\infty} \hat{\sigma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) \cdot \hat{o}(\mathbf{o}+s\mathbf{d}, \mathbf{c}) \cdot \hat{\gamma}(\mathbf{o}+s\mathbf{d}|\mathbf{C}_t) ds$$

其中：
- $\mathbf{o}$ 为相机光心，$\mathbf{d}$ 为像素 $\mathbf{p}$ 对应的光线方向；
- $\hat{\sigma}(\cdot|\mathbf{C}_t)$：占用模型预测的占用概率，替代原积分中的表面指示函数 $\sigma$；
- $\hat{o}(\cdot, \mathbf{c})$：可见性近似项，在体积渲染框架下通过沿光线累积的透过率 $T(s)$ 自然体现；
- $\hat{\gamma}(\cdot|\mathbf{C}_t)$：新颖性场，标记该空间位置是否已被先前观测覆盖。

这一重构的意义在于：原本需要在三维表面上进行的复杂积分，现在可以转化为沿像素光线的体积渲染，从而直接利用 GPU 加速的光栅化管线进行高效计算。

### Imagined Gaussians：从占用场到可渲染表征

为实现上述体积渲染，MAGICIAN 将占用场转化为 3D 高斯泼溅表征，称为 **Imagined Gaussians**。具体而言，从占用模型预测的占用场中采样一组 3D 高斯，其中：
- **高斯透明度**编码占用概率 $\hat{\sigma}$：占用概率越高的区域，高斯越不透明；
- **高斯颜色**编码二进制新颖性 $\hat{\gamma}$：新颖区域为亮色，已观测区域为暗色。

通过这一设计，对候选位姿 $\mathbf{c}$ 渲染得到的像素级新颖性图 $I_{\text{novelty}}(\mathbf{p})$ 直接对应式 (4) 的积分结果。最终的渲染覆盖增益为所有有效像素的深度加权求和：

$$G_{\text{rendered}}(\mathbf{c}) = \sum_{\mathbf{p} \in \mathcal{P}_{\text{valid}}} w_{\text{depth}}(\mathbf{p}) I_{\text{novelty}}(\mathbf{p})$$

其中深度加权因子：

$$w_{\text{depth}}(\mathbf{p}) = \min\left(1, \left(\frac{D(\mathbf{p})}{D_{\text{th}}}\right)^2\right)$$

用于防止近距离像素因投影面积小而导致的覆盖贡献低估，$D(\mathbf{p})$ 为该像素的渲染深度，$D_{\text{th}}$ 为深度阈值。

这一计算流程（Figure 3 示意）将每次覆盖增益评估的时间从 MACARONS 蒙特卡洛方法的约 0.05 秒降至约 0.002 秒，实现 **25 倍加速**，为束搜索中的大量候选轨迹评估提供了实时可行性。

### 束搜索长期规划

规划模块的目标是在离散动作空间中优化长期轨迹的累积覆盖增益：

$$G(\tau) = \sum_{i=1}^{N_d} G(\mathbf{c}_{t+i})$$

其中 $\tau = \{\mathbf{c}_{t+1}, \ldots, \mathbf{c}_{t+N_d}\}$ 为长度为 $N_d$ 的候选轨迹。

束搜索以增量方式构建候选轨迹：从当前位姿出发，每一步扩展所有可能的动作（如前进、左转、右转），对每个候选位姿通过 Imagined Gaussians 渲染计算覆盖增益，并更新对应束的新颖性状态（将已观测区域的 $\hat{\gamma}$ 置零），仅保留累积增益最高的 $N_b$ 条束继续扩展。最终选择累积覆盖增益最高的轨迹执行前 $N_f$ 步，随后触发下一轮重规划。

消融实验证实，将束宽 $N_b$ 从 1 增至 10、前瞻步数 $N_d$ 从 1 增至 10 时，AUC 绝对提升 6.3%，最终覆盖率绝对提升 9.3%，有力验证了长期规划相对于贪心单步选择的显著优势。值得注意的是，即使仅在贪心设置下（$N_b = N_d = 1$），MAGICIAN 的体积渲染方法仍比 MACARONS 的蒙特卡洛方法在 AUC 上高出 5.2%，在最终覆盖率上高出 10.9%，表明覆盖增益估算精度的提升本身即带来可观的性能增益。

## 实验与关键发现

### 实验配置

MAGICIAN在两个大规模基准数据集上进行评估：**Macarons++**（包含户外场景）和**Matterport3D (MP3D)**（包含室内场景）。实验配置如 Table 1 所示，MP3D上分别测试了轮式机器人和无人机两种动作空间设置——轮式机器人动作为前进(6.5 cm)和转向(±10°)，无人机则具有更自由的3D运动能力。所有方法在每个场景使用相同的五个随机初始相机位姿，保证对比公平性。评估指标包括**AUC**（Area Under the Coverage curve，反映探索效率）和**最终覆盖率**（Final Coverage），两者均基于从所有可达视角渲染生成的点云真值计算。

默认超参数设置为：束搜索宽度 $N_b = 10$，前瞻步数 $N_d = 10$，每执行 $N_f = 1$ 步后重新规划。

### 主要结果

#### Macarons++ 基准

Table 2 展示了Macarons++数据集上的核心对比结果。MAGICIAN在AUC指标上达到 **0.721**，相比最强的基线方法MACARONS的0.647提升 **+0.074**（相对提升11.4%）；在最终覆盖率上达到 **0.919**，相比MACARONS的0.819绝对提升 **10个百分点**，相对提升12.2%。这一显著提升验证了长期规划策略相比贪心单步NBV方法的根本优势。

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/008_Table_2.jpg]]
*Table 2: Evaluation results on the Macarons++ dataset*

与各类基线方法的对比显示：
- 传统贪心覆盖增益方法**SCONE**和基于学习的**MACARONS**受限于短视决策，探索效率明显低于MAGICIAN
- 基于前沿和Fisher信息的方法**FisherRF**以及前沿探索基线**FBE**在覆盖率上均显著落后
- 学习预测路径覆盖增益的**NBP**方法同样无法匹敌MAGICIAN的长期规划能力
- **随机游走**基线表现最差，验证了主动探索策略的必要性

各场景详细结果见 Table 6（AUC）和 Table 7（最终覆盖率），MAGICIAN在绝大多数场景上保持领先。

#### MP3D 基准

Table 4 展示了MP3D数据集上的结果。在轮式机器人设置下，MAGICIAN达到 **85.45%** 的完成率（Comp.），超过NBP的79.38%达 **+6.07个百分点**；在无人机设置下达到 **96.83%**，超过ActiveGamer的95.32%。值得注意的是，MP3D上的MAGICIAN直接使用预训练模型，未在室内场景上进行额外微调，而部分基线方法需要场景特定的微调——这体现了预训练占用模型的强泛化能力。

#### 重建质量评估

Table 3 展示了基于探索轨迹采集的100张RGB图像进行新视角合成和网格重建的定量结果。MAGICIAN在所有指标上均达到最优，包括PSNR、SSIM、LPIPS（渲染质量）以及Chamfer Distance、Normal Consistency（几何精度）。Figure 5 和 Figure 6 的定性对比直观展示了MAGICIAN轨迹带来的重建完整性优势——其他方法的重建结果常出现孔洞和噪声，而MAGICIAN能覆盖整个场景表面，生成完整准确的面片网格。

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of novel view synthesis (top row) and surface reconstruction (bottom row) in outdoor and indoor scenes. For each method, we show RGB Gaussian splatting renderings and normal maps of reconstructed meshes after applying Mesh-Inthe-Loop Gaussian Splatting [20] on 100 images collected along the trajectory. The trajectories computed with our method produce more accurate and complete reconstructions, resulting in better rendering quality and preventing holes in reconstructed surfaces*

#### 鲁棒性分析

Figure 9 展示了各方法在不同场景和随机初始位姿下最终覆盖率的标准差。MAGICIAN的覆盖率标准差始终保持在较低水平，表明其对初始条件具有较强的鲁棒性，而其他方法则表现出更大的波动。在位姿噪声测试中（$\sigma = 0.5\text{m}$ 平移，$3^\circ$ 旋转），MAGICIAN的AUC仅下降0.28个百分点，覆盖率下降1.12个百分点，进一步验证了对位姿不确定性的鲁棒性。

### 消融实验

#### 长期规划的有效性

Figure 7 和 Table 8 系统消融了束搜索参数的影响。当束搜索宽度从1增至10、前瞻步数从1增至10时，AUC绝对提升 **6.3%**，最终覆盖率绝对提升 **9.3%**。这一结果直接证明了长期规划相对于贪心策略（束宽=1，前行步数=1）的显著优势。值得注意的是，即使仅使用贪心NBV设置（束宽=1，前行步数=1），MAGICIAN的Imagined Gaussians体积渲染方法仍比MACARONS的蒙特卡洛方法AUC高 **5.2%**，最终覆盖率高 **10.9%**，表明体积渲染近似本身就在单步评估质量上优于蒙特卡洛采样。

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/012_Figure_7.jpg]]
*Figure 7: Ablation study on the beam search parameters. The horizontal axis denotes the beam width*

#### 计算效率

覆盖增益计算速度是长期规划可行性的关键瓶颈。MAGICIAN的Imagined Gaussians将单次覆盖增益计算时间从MACARONS蒙特卡洛方法的 **0.05秒** 降至 **0.002秒**，实现 **25倍加速**。这一加速使得在束搜索中高效评估大量候选轨迹成为可能——以束宽10、前瞻步数10为例，每轮规划需评估数百个候选位姿，25倍加速将评估时间从不可接受的数十秒降至秒级。

#### 重规划频率

Figure 8 消融了重规划频率 $N_f$ 的影响。结果显示，每6步重新规划即可达到SOTA性能，而每步重规划（$N_f = 1$）仅带来微小额外提升。这表明MAGICIAN的长期规划本身已具备足够的开环鲁棒性，适度的闭环重规划即可有效修正累积偏差，在计算开销和性能之间取得良好平衡。

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/010_Figure_8.jpg]]
*Figure 8: Ablation study on replanning frequency. The horizontal axis indicates the number*

#### 占用模型泛化性

Table 5 对比了预训练模型与在室内场景上微调模型的性能。微调版本在最终覆盖率上仅有0.5%的微小提升，而预训练模型在探索效率（AUC）上反而更高（0.652 vs 0.646）。这表明预训练占用模型已具备良好的跨场景泛化能力，无需针对特定环境重新训练。

![[assets/figures/papers/paper_list_l2057_https_arxiv_org_abs_2603_22650/figures/013_Table_5.jpg]]
*Table 5: Ablation study on comparing models with and without fine-tuning on indoor environments. The fine-tuned version shows a minor 0.5% improvement in final coverage, while the original model retains higher exploration efficiency*

#### 代理点采样密度

Table 9 消融了用于占用场查询的代理点采样密度。1×密度（原始设置）即可兼顾精度与效率；2×和4×密度虽有小幅性能提升，但计算开销显著增大。这一结果验证了默认采样密度的合理性。

### 失败模式与局限性

尽管MAGICIAN展现出优异性能，分析揭示了几类需要关注的局限：

1. **探索初期的冷启动问题**：在观测极度稀疏的探索初期，占用模型预测精度不足，可能导致初始路径选择次优。Figure 4 展示了Imagined Gaussians随探索进程逐步与地面真值网格对齐的过程，早期阶段的高斯分布较为弥散。闭环重规划机制可逐步缓解此问题，但无法完全消除早期效率损失。

2. **传感器依赖**：当前方法依赖RGB-D输入和已知位姿。在纯RGB或位姿估计误差更大的场景下，占用预测和覆盖增益计算的可靠性将下降，需要进一步研究。

3. **动作空间离散化**：束搜索在离散动作空间上运行高效，但连续高维动作空间（如空中机器人的3D轨迹规划）下的扩展性尚待验证。当前离散化策略在无人机设置下仍取得了有竞争力的结果，但更复杂的机动能力可能带来额外增益。

4. **全局结构先验的局限**：占用模型基于局部几何特征预测，在极度稀疏观测时可能无法提供可靠的全局结构先验。这在大型开放场景或结构高度对称的环境中尤为明显，可能导致探索路径的全局次优性。

## 定位与知识库关联

### 1. 方法在主动建图谱系中的位置

MAGICIAN 处于**主动三维建图**（active 3D mapping）与**次最佳视角规划**（Next-Best-View, NBV）的交汇点，其核心贡献在于将长期轨迹优化引入该领域，同时通过“想象高斯”（Imagined Gaussians）将覆盖增益评估重构为可微分的体积渲染问题。

从方法谱系来看，主动建图规划可沿两条轴线分类：

**轴线一：规划视野的跨度。**

- **单步贪心方法**构成早期主流。**SCONE** 和 **MACARONS** 在每个决策步仅评估当前候选视角的即时覆盖增益，选择局部最优。这类方法计算轻量但缺乏前瞻性，容易陷入局部最优，导致重复路径和遗漏区域。论文实验证实，MACARONS 在 Macarons++ 上的最终覆盖率仅为 0.819，而 MAGICIAN 达到 0.919（Table 2），绝对差距 10 个百分点。
- **短序列方法**尝试弥补贪心缺陷。**NBP** 学习预测两视点间路径的覆盖增益，但仍局限于两步推理，无法建模更长期的探索因果链。
- **MAGICIAN 的长期束搜索**将规划视野扩展至 $N_d = 10$ 步，通过束搜索在 $N_b = 10$ 条候选轨迹中并行评估累积覆盖增益 $G(\tau) = \sum_{i=1}^{N_d} G(\mathbf{c}_{t+i})$，是主动建图中首个实现长期轨迹优化的框架。

**轴线二：覆盖增益的计算范式。**

- **蒙特卡洛采样派**（以 MACARONS 为代表）对占用网络和新颖性网络进行大量采样积分，每次候选位姿评估耗时约 0.05 秒。精度尚可但速度瓶颈严重制约了束搜索中大量候选轨迹的实时评估。
- **体素/前沿派**（如 **FBE**、**UPEN**）基于显式占用场或前沿边界进行探索，计算快速但难以精确量化表面覆盖增益。
- **MAGICIAN 的体积渲染派**揭示了覆盖增益积分与体积渲染方程的结构等价性——将占用概率 $\hat{\sigma}$ 作为密度场、新颖性 $\hat{\gamma}$ 作为颜色场、透过率近似遮挡——从而将评估转化为 3D 高斯泼溅的光栅化渲染，速度提升 25 倍（0.002 秒/次），使长期束搜索在计算上变得可行。

### 2. 与关键基线工作的关系

**与 MACARONS 的关系：继承与超越。** MAGICIAN 直接沿用了 MACARONS 的神经占用预测模型架构（多层 Transformer，在 ShapeNet 预训练后在 3D 场景上微调），但在两个关键维度上实现了根本性超越：（1）将覆盖增益计算从蒙特卡洛积分改造为体积渲染，获得 25 倍加速；（2）从贪心单步决策升级为束搜索长期规划。消融实验表明，即使将 MAGICIAN 退化为贪心模式（束宽 = 前行步数 = 1），其 AUC 仍比 MACARONS 高 5.2%，最终覆盖率高 10.9%，证明体积渲染方法本身优于蒙特卡洛近似。

**与 ActiveGamer 的关系：3D 高斯泼溅的不同用途。** **ActiveGamer** 将 3D 高斯泼溅用于场景重建和视角质量评估，而 MAGICIAN 的“想象高斯”用于编码**未知区域的几何先验和不确定性**——高斯透明度编码占用概率，颜色编码新颖性。两者虽共享 3DGS 渲染管线，但语义和目标截然不同。在 Matterport3D 无人机设置下，MAGICIAN 的完成率（96.83%）略优于 ActiveGamer（95.32%），在轮式机器人设置下优势更为显著（85.45% vs 次优方法 NBP 的 79.38%）。

**与 FisherRF 和 NARUTO 的关系：信息论视角的差异。** **FisherRF** 基于 Fisher 信息评价路径的信息增益，**NARUTO** 针对 NeRF 重建进行主动视角选择。这些方法关注重建不确定性最小化，而 MAGICIAN 直接优化表面覆盖增益——一个更贴近“建图完整性”本质的目标。

### 3. 适用边界与关键假设

MAGICIAN 的有效性建立在一组明确假设之上，这些假设同时界定了其适用边界：

1. **RGB-D 观测与已知位姿。** 方法依赖深度传感器提供几何约束，且假设相机位姿已知。在纯 RGB 探索或位姿估计噪声较大的场景（如快速运动的无人机），性能可能下降。消融实验显示，在位姿噪声（$\sigma=0.5$m 平移，3° 旋转）下，AUC 仅下降 0.28 个百分点，覆盖率下降 1.12 个百分点，表明对位姿不确定性具有一定鲁棒性，但极端情况仍需验证。

2. **预训练占用模型的泛化能力。** 占用模型在 ShapeNet 上预训练、在 3D 场景上微调，为“想象高斯”提供结构先验。在 Matterport3D 室内场景上的实验表明，额外微调对性能无显著提升（预训练 AUC 0.652 vs 微调 0.646），说明预训练模型已具备良好的跨场景泛化性。但在与训练数据分布差异极大的环境（如水下、太空）中，占用预测精度可能不足。

3. **离散动作空间。** 束搜索在离散候选位姿集合上展开（轮式机器人：前进/转向；无人机：离散航点）。连续高维动作空间下的扩展性尚待验证，直接离散化可能导致候选数量指数爆炸。

4. **静态场景假设。** 方法假设场景在探索过程中保持不变。动态物体（行人、移动家具）会破坏“想象高斯”的几何先验和新颖性状态管理，导致规划失效。

### 4. 局限性与失败模式

**探索初期的冷启动问题。** 当观测极度稀疏时，占用模型缺乏足够的局部几何线索来预测可靠的全局结构先验。这可能导致初始几条轨迹的路径选择次优。论文在附录 C 中承认此问题，并指出闭环重规划可逐步缓解——随着探索推进，观测积累使“想象高斯”与真实几何的对齐程度持续改善（Figure 4 展示了这一演化过程）。

**占用模型的结构先验盲区。** 占用模型基于局部几何特征预测，可能无法捕捉需要全局语义理解的结构（如细长走廊尽头的房间、被遮挡的夹层）。在这些场景中，“想象高斯”可能低估或完全遗漏未观测区域，导致束搜索错过高价值路径。

**束搜索的局部最优风险。** 尽管束搜索比贪心方法更具前瞻性，但在复杂场景中仍可能陷入局部最优——所有束可能被相似的“诱惑性”区域吸引，集体忽略其他高价值区域。增大束宽可缓解此问题（Figure 7 显示束宽从 1 增至 10 时 AUC 提升 6.3%），但计算开销线性增长。

**深度加权因子的启发式性质。** 覆盖增益计算中的深度加权因子 $w_{\mathrm{depth}}(\mathbf{p}) = \min(1, (D(\mathbf{p})/D_{\mathrm{th}})^2)$ 用于防止近距离过度采样导致增益虚高，但其阈值 $D_{\mathrm{th}}$ 的选择是启发式的，可能在不同场景尺度下需要调整。

### 5. 开放问题与未来方向

1. **纯 RGB 探索的可行性。** 能否将“想象高斯”与单目深度估计或神经辐射场的不确定性结合，取消对深度传感器的依赖？这将显著扩展方法的硬件适用范围（如消费级手机、轻量无人机）。

2. **三维基础模型的先验注入。** 以 LRM、3DGen 为代表的三维生成基础模型正在快速发展，它们从单张或少量图像中推理完整三维结构的能力，有望为占用预测提供更强的语义和几何先验。将此类模型作为“想象高斯”的初始化或条件信号，可能大幅提升稀疏观测下的规划质量。

3. **动态场景的自适应探索。** 如何使“想象高斯”和长期规划适应场景中的动态变化？可能的思路包括：为高斯引入时间衰减因子，使过时的新颖性状态自动失效；或将动态物体检测与局部重规划结合。

4. **连续动作空间的扩展。** 将束搜索扩展到连续高维动作空间（如空中机器人的 6-DoF 轨迹规划）而不丧失计算效率，是一个开放挑战。可能的路径包括：在连续空间中采样候选动作并结合学习型价值函数剪枝，或使用模型预测控制（MPC）框架将“想象高斯”渲染作为可微分的代价函数。

5. **多智能体协同探索。** 当前方法针对单智能体设计。在多智能体场景中，如何协调多个“想象高斯”状态、避免探索冗余并最大化集体覆盖效率，是自然延伸方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/MAGICIAN_Efficient_Long_Term_Planning_with_Imagined_Gaussians_for_Active_Mapping.pdf]]
