---
title: "SPREAD: Spatial-Physical REasoning via geometry Aware Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SPREAD_Spatial_Physical_REasoning_via_geometry_Aware_Diffusion.pdf
project_link: null
code_link: null
aliases:
- SPREAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将空间关系（如“左侧”）和物理关系（如“支撑”）建模为可微分图先验，并引入网格级碰撞避免、重力以及关系指导等多指导信号，SPREAD在扩散生成过程中显式地施加物理约束，从而因果地控制场景的物理合理性。
primary_logic: 图Transformer联合学习对象间的空间和物理关系，并与几何感知模块（基于感知器和有向Chamfer距离）协同工作，使得扩散模型能够在保持关系一致性的同时，生成物理上无缝衔接、可直接用于仿真的3D场景。
claims:
- 在ProcTHOR数据集上，SPREAD将网格碰撞率（Col_mesh）从基线最佳的0.260降至0.121。
- 在ProcTHOR上，SPREAD取得了最高的图召回率（GRecall 0.979），优于InstructScene的0.964。
- 平均支撑距离（ASD）从0.021降至0.007，表明物体支撑更精确。
- 物理仿真稳定性（Isaac Stability）从0.876提升至0.950，场景崩溃最少。
---

# SPREAD: Spatial-Physical REasoning via geometry Aware Diffusion

> [!tip] 核心洞察
> 图Transformer联合学习对象间的空间和物理关系，并与几何感知模块（基于感知器和有向Chamfer距离）协同工作，使得扩散模型能够在保持关系一致性的同时，生成物理上无缝衔接、可直接用于仿真的3D场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | SPREAD: 面向空间-物理推理的几何感知扩散框架 |
| 英文题名 | SPREAD: Spatial-Physical REasoning via geometry Aware Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27573) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SPREAD |
| Dataset | 3D-FRONT, ProcTHOR |

> [!tip] 效果简介
> - 3D-FRONT (Bedroom) 上，Col_mesh 0.097 vs 0.275 (ATISS) (-0.178)。
> - 3D-FRONT (Livingroom) 上，Col_mesh 0.185 vs 0.350 (InstructScene) (-0.165)。
> - 3D-FRONT (Diningroom) 上，Col_mesh 0.183 vs 0.331 (InstructScene) (-0.148)。

## 概述

现有3D场景生成方法在视觉质量上取得了显著进展，但普遍面临一个关键瓶颈：它们依赖结构化的训练数据，缺乏对复杂空间关系和物理交互（如支撑、碰撞）的显式建模，导致生成的场景常出现物体悬浮、穿透等物理不可信现象。SPREAD正是针对这一问题而提出的。

SPREAD的核心思路是将空间关系（如“左侧”、“上方”）和物理关系（如“支撑”）建模为可微分的图先验，并与扩散模型深度融合。通过图Transformer联合学习对象间的空间-物理关系，再结合几何感知模块（基于感知器与有向Chamfer距离）和多引导信号（碰撞避免、重力、关系约束），SPREAD在扩散生成过程中显式地施加物理约束，从而因果性地控制场景的物理合理性。

在3D-FRONT和ProcTHOR两个数据集上的实验表明，SPREAD在物理合理性指标上全面超越现有方法：网格碰撞率（Col_mesh）在ProcTHOR上从0.260降至0.121，平均支撑距离（ASD）从0.021降至0.007，物理仿真稳定性（Isaac Stability）从0.876提升至0.950，同时取得了最高的图召回率（GRecall 0.979）。用户调研中，SPREAD以88.6%的得票率显著优于ATISS（0.9%）、InstructScene（4.4%）和DiffuScene（6.1%），主观评价其物理一致性和场景合理性最优。

## 背景与动机

### 3D场景生成中的物理合理性瓶颈

生成逼真的3D室内场景是具身AI、仿真环境和内容创作领域的核心需求。然而，现有方法普遍面临一个关键瓶颈：**生成的场景在物理上不可信**。物体悬浮于半空、网格相互穿透、支撑关系错乱等现象频繁出现，使得生成的场景无法直接用于物理仿真或机器人交互。这一问题的根源在于，当前主流的3D场景生成方法——无论是自回归模型（如**ATISS**）、基于扩散的模型（如**DiffuScene**），还是两阶段语义图解码方法（如**InstructScene**）——都依赖有限且结构化程度较高的训练数据，缺乏对复杂空间关系和物理交互（如支撑、碰撞）的显式建模。

具体而言，现有方法的缺陷体现在三个层面：

1. **几何感知缺失**：基线方法通常使用隐式形状嵌入或仅依赖类别标签进行布局生成，无法感知当前时间步下物体网格级别的实际几何状态。这意味着扩散过程在去噪时“看不见”物体的真实表面，自然无法避免穿透。
2. **碰撞处理粗糙**：多数方法要么忽略碰撞，要么仅依赖包围盒（bounding box）近似进行碰撞检测。包围盒无法捕捉复杂几何体的精细交互，导致生成的场景在网格级别仍存在大量穿透。
3. **物理约束空白**：现有方法缺乏对重力、支撑关系等基本物理约束的显式建模。物体可以任意悬浮，支撑物与被支撑物之间没有精确的接触约束，导致场景在物理仿真中迅速崩溃。

### 从“看起来合理”到“物理上成立”的跨越

上述缺陷揭示了一个更深层的认知鸿沟：当前生成模型追求的是视觉层面的“合理性”（plausibility），而非物理层面的“成立性”（validity）。FID等视觉质量指标可以评估布局的统计分布是否与真实数据接近，但无法反映场景是否经得起物理规律的检验。这导致了一个悖论：一个FID得分优秀的场景，可能在Isaac Sim中因重力作用而瞬间坍塌。

SPREAD正是针对这一鸿沟提出的解决方案。其核心动机在于：**将空间关系（如“左侧”、“上方”）和物理关系（如“支撑”、“接触”）建模为可微分的图先验，并在扩散生成过程中显式施加物理约束，从而因果性地控制场景的物理合理性**。通过这一范式转换，SPREAD旨在使生成模型不仅能“画”出合理的布局，更能“理解”并“遵守”物理世界的规则，产出可直接用于仿真的3D环境。

## 核心创新

SPREAD的核心创新在于将**空间关系**与**物理交互**显式地建模为可微分的图先验，并将其深度嵌入扩散模型的生成过程，从而因果性地解决了现有方法普遍存在的物体悬浮、穿透等物理不可信问题。与依赖隐式形状嵌入或仅使用类别标签的基线方法（如ATISS、DiffuScene、InstructScene）不同，SPREAD通过以下四个关键维度的创新，实现了从“视觉合理”到“物理可信”的跨越。

### 1. 显式空间-物理关系图先验

现有方法通常将场景生成视为无约束的布局优化问题，忽略了物体间丰富的交互关系。SPREAD首次将空间关系（如“左侧”、“上方”）和物理关系（如“支撑”）分别建模为图结构 $\mathcal{G}_{\rho}$ 和 $\mathcal{G}_{\kappa}$，并将其作为扩散图块的偏置输入。具体而言，图Transformer的每一层更新遵循：

$$\mathbf{H}_t^{l+1} = \mathrm{GraphBlock}^l(\mathbf{H}_t^l, \mathcal{G}_\rho, \mathcal{G}_\kappa)$$

这使得模型在去噪过程中始终感知到物体间的显式关系约束，从而在保持关系一致性的同时生成物理上合理的布局。这一设计直接带来了图召回率（GRecall）的显著提升——在ProcTHOR数据集上达到0.979，优于InstructScene的0.964（Table 1）。

### 2. 几何感知机制：从包围盒到网格级感知

基线方法（如ATISS、DiffuScene）通常依赖包围盒近似或完全忽略碰撞，无法感知物体在扩散过程中的实时几何状态。SPREAD在每个扩散时间步对每个物体采样 $M=2000$ 个表面点，计算有向Chamfer距离：

$$d_{\mathrm{scd}}(\mathbf{p}) = \min_{\mathbf{q}\in\mathcal{P}_{\neg i}} \|\mathbf{p}-\mathbf{q}\|_2 \cdot \mathrm{sign}(\mathbf{n}_{\mathrm{nn}}^{\top}(\mathbf{p}-\mathbf{q}))$$

该特征不仅编码了点对点距离，还通过法线方向区分“穿透”与“分离”状态，形成形状为 $(B, N, M, 4)$ 的特征张量。随后，感知器（Perceiver）模块通过交叉注意力将稀疏高维特征压缩为固定数量的几何令牌 $f^{geo}$，使模型能够以较低计算成本感知网格级的碰撞与穿透。消融实验证实，仅添加此模块即可将网格碰撞率（Col_mesh）从0.241降至0.225，仿真稳定性从0.934提升至0.938（Table 2）。

### 3. 多引导框架：可微物理约束的组合优化

与基线方法缺乏显式物理约束或仅使用单一碰撞引导不同，SPREAD提出了一个多引导框架，在推理时通过调节得分函数来施加物理约束：

$$\nabla_{\mathbf{x_t}} \log p_\gamma(\mathbf{x_t}) = s_\theta(\mathbf{x_t}, t) + \gamma \nabla_{\mathbf{x_t}} \mathcal{G}(\mathbf{x_t})$$

其中组合引导信号 $\mathcal{G}$ 由三项加权构成：

$$\mathcal{G} = \lambda_C \mathcal{G}_C + \lambda_H \mathcal{G}_H + \lambda_R \mathcal{G}_R$$

- **碰撞引导** $\mathcal{G}_C$：基于三角形对的锥形距离场（CoDF），惩罚网格相交
- **重力引导** $\mathcal{G}_H$：惩罚超出容忍高度的悬浮或穿透，确保物体着地
- **关系引导** $\mathcal{G}_R$：惩罚支撑关系中物体外顶点到支撑凸包的距离，确保“物有所依”

三项引导的联合权重分别为 $7.5\times10^{-3}$、$1\times10^{-3}$ 和 $1\times10^{-3}$。这一多信号协同机制使得SPREAD在ProcTHOR上将网格碰撞率从基线最佳的0.260（InstructScene）降至0.121，平均支撑距离（ASD）从0.021降至0.007，仿真稳定性从0.876提升至0.950（Table 1）。

### 4. 预训练形状编码器：稳定的几何先验

SPREAD采用预训练的**Michelangelo**形状编码器提取256个64维的形状令牌，在扩散过程中保持不变。与普通形状编码器相比，Michelangelo能更好地捕获底层几何信息，对网格碰撞率有适度改善（Section 9），为几何感知模块提供了稳定的形状先验基础。

### 创新总结

上述四个创新维度形成了完整的因果链条：**图先验**提供关系骨架，**几何感知**注入实时网格信息，**多引导框架**施加物理约束，**预训练编码器**保障几何质量。这一协同设计使得SPREAD在用户调研中以88.6%的得票率显著优于ATISS（0.9%）、InstructScene（4.4%）和DiffuScene（6.1%），主观评价其物理一致性和场景合理性最佳（Figure 6）。

## 整体框架

SPREAD 是一个以**空间图与物理图为可微分先验**的条件扩散框架，其核心设计目标是在生成 3D 场景布局的同时，显式地保证物体间的物理合理性——消除穿透、悬浮等常见伪影。

### 输入输出流

框架的输入由两部分构成：

1. **场景图先验**：用户或系统提供两个关系图——
   - 空间关系图 $\mathcal{G}_{\rho} \in \{0, \dots, m\}^{N \times N}$，编码物体间的方位关系（如“左侧”、“前方”）；
   - 物理关系图 $\mathcal{G}_{\kappa}$，编码支撑等物理交互。  
   这两个图通过嵌入层与 MLP 映射为连续的边嵌入 $\mathbf{E}$，作为扩散图块的偏置输入。

2. **形状先验**：每个物体使用预训练的 **Michelangelo 形状编码器** 提取 256 个 64 维的形状令牌，在扩散过程中保持固定，提供稳定的几何先验。

输出为 $N$ 个物体的 9 维位姿向量（3 维平移 + 6 维旋转），即联合状态空间：

$$\mathbf{x}_0 = \bigoplus_{j=1}^{N} [p_j^i \lVert r_j^i] \in \mathbb{R}^{N \times (3+6)}$$

### 核心 Pipeline 模块关系

SPREAD 的生成流程围绕**图条件扩散**展开，关键模块包括：

| 模块 | 角色 | 证据锚点 |
|------|------|----------|
| **图 Transformer（L 层 Graph Block）** | 融合节点特征、静态形状令牌与动态几何嵌入，沿空间/物理边执行图注意力传播，实现关系条件化去噪 | Section 3.3, 公式(4) |
| **有向 Chamfer 距离计算** | 每个去噪步对每个物体采样 $M=2000$ 个表面点，计算到其他物体点云的有向最小距离 $d_{\mathrm{scd}}$，形成 $(B, N, M, 4)$ 特征张量 | Section 3.3, 公式(5) |
| **几何感知器模块（Perceiver）** | 通过交叉注意力将稀疏高维几何特征压缩为 $n$ 个 $d$ 维几何令牌 $\mathbf{f}^{\mathrm{geo}}$，感知碰撞与穿透 | Section 3.3 |
| **多引导框架** | 在推理时组合碰撞引导（CoDF）、重力引导（高度阈值惩罚）和关系引导（支撑外顶点距离惩罚），通过 $\nabla_{\mathbf{x_t}} \mathcal{G}(\mathbf{x_t})$ 调节得分函数 | Section 3.4, 公式(6)(7) |

### 生成流程

1. **前向扩散**：将真实位姿 $\mathbf{x}_0$ 按 Markov 高斯转移逐步加噪至 $\mathbf{x}_T$：
   $$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

2. **图条件去噪**：图 Transformer 在每一层接收当前状态 $\mathbf{H}_t^l$ 以及空间/物理图 $\mathcal{G}_{\rho}, \mathcal{G}_{\kappa}$，输出更新后的特征：
   $$\mathbf{H}_t^{l+1} = \mathrm{GraphBlock}^l(\mathbf{H}_t^l, \mathcal{G}_{\rho}, \mathcal{G}_{\kappa})$$

3. **几何感知注入**：每个去噪步计算有向 Chamfer 距离，经 Perceiver 压缩为几何令牌，注入图 Transformer 的节点特征中，使模型能感知当前时间步的网格级几何状态。

4. **多引导逆向过程**：推理时，得分函数由组合引导信号调节：
   $$\nabla_{\mathbf{x_t}} \log p_\gamma(\mathbf{x_t}) = s_\theta(\mathbf{x_t}, t) + \gamma \nabla_{\mathbf{x_t}} \mathcal{G}(\mathbf{x_t})$$
   其中 $\mathcal{G} = \lambda_C \mathcal{G}_C + \lambda_H \mathcal{G}_H + \lambda_R \mathcal{G}_R$，权重分别为 $7.5\times10^{-3}$、$1\times10^{-3}$、$1\times10^{-3}$。

### 与基线方法的本质差异

与现有方法相比，SPREAD 在三个关键维度上做出了根本性改变：

- **几何感知机制**：基线方法（如 ATISS、DiffuScene）依赖隐式形状嵌入或类别标签，无法感知当前时间步的网格级几何状态；SPREAD 在每个去噪步采样表面点并计算有向 Chamfer 距离，通过 Perceiver 提取动态几何特征。
- **碰撞处理**：基线方法依赖包围盒近似或完全忽略碰撞；SPREAD 使用网格级三角形交叉检测，以锥形距离场（CoDF）作为可微碰撞指导。
- **物理约束建模**：基线方法缺乏显式物理约束；SPREAD 将空间和物理关系建模为显式图结构，并与重力引导、支撑关系引导协同工作，因果地控制场景的物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SPREAD. We propose SPREAD, a diffusion-based framework for generating physically plausible 3D scenes, which integrates relational constraints through spatial (Gρ) and physical graphs (Gκ) while leveraging geometric perception via Perceiver Layers. The model employs graph-attention guided diffusion to jointly optimize physical plausibility and spatial relations during generation, producing realistic scenes with natural object interactions*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of SPREAD, a diffusion-based framework for generating physically plausible 3D scenes with rich object interactions. (A) SPREAD synthesizes detailed object-level layouts with natural spatial and physical interactions, going beyond coarse layout arrangements. (B) SPREAD faithfully adheres to provided spatial and physical graph priors, G. (C) SPREAD can provide simulationready environments for embodied AI agents*

## 核心模块与公式推导

### 扩散状态空间与图条件化

SPREAD 将场景生成建模为对 $N$ 个物体联合状态的条件扩散过程。每个物体的状态由其 3D 平移向量 $p_j^i \in \mathbb{R}^3$ 和 6D 连续旋转表示 $r_j^i \in \mathbb{R}^6$ 组成，所有物体的状态拼接为扩散的初始状态：

$$
\mathbf{x}_0 = \bigoplus_{j=1}^{N} [p_j^i \lVert r_j^i] \in \mathbb{R}^{N \times (3+6)}
$$

前向扩散过程遵循标准的 Markov 高斯转移：

$$
q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})
$$

其中 $\beta_t$ 为噪声调度参数。

**图条件化机制**是 SPREAD 区别于常规扩散场景生成方法的核心。论文将空间关系（如“左侧”、“前方”）和物理关系（如“支撑”、“接触”）分别建模为空间关系图 $\mathcal{G}_\rho$ 和物理关系图 $\mathcal{G}_\kappa$，二者作为可微分图先验注入去噪过程。具体地，离散图关系通过嵌入层映射为连续潜在表示：

$$
\mathbf{E} = \mathbf{MLP}(\operatorname{Embedding}(\mathcal{G}))
$$

在图 Transformer 的每一层中，节点特征沿显式边进行图注意力传播，同时融合空间和物理关系：

$$
\mathbf{H}_t^{l+1} = \mathrm{GraphBlock}^l(\mathbf{H}_t^l, \mathcal{G}_\rho, \mathcal{G}_\kappa)
$$

这种设计使得去噪网络在每一步都能感知物体间的关系约束，从而因果地控制生成场景的结构一致性。

### 几何感知模块

现有方法通常依赖隐式形状嵌入或仅使用类别标签，无法感知当前时间步的网格级几何状态。SPREAD 的核心创新在于引入**几何感知模块**，在每个扩散时间步显式计算物体间的空间干涉。

**有向 Chamfer 距离**。对每个物体，采样 $M=2000$ 个表面点，计算其到其他物体点云的有向最小距离：

$$
d_{\mathrm{scd}}(\mathbf{p}) = \min_{\mathbf{q}\in\mathcal{P}_{\neg i}} \|\mathbf{p}-\mathbf{q}\|_2 \cdot \mathrm{sign}(\mathbf{n}_{\mathrm{nn}}^{\top}(\mathbf{p}-\mathbf{q}))
$$

其中 $\mathbf{n}_{\mathrm{nn}}$ 是最近点 $\mathbf{q}$ 处的法向量，符号项使得该距离能区分穿透（负值）与分离（正值）。这一操作产生形状为 $(B, N, M, 4)$ 的特征张量，前三个通道编码全局坐标，第四通道编码 $d_{\mathrm{scd}}$。

**感知器压缩**。稀疏的高维几何特征通过感知器（Perceiver）模块，经交叉注意力压缩为 $n$ 个 $d$ 维几何令牌 $\mathbf{f}^{geo}$。与普通 Transformer 相比，感知器在相同性能下计算成本更低、网络结构更浅。这些几何令牌与静态形状令牌（由预训练的 Michelangelo 编码器提取的 $256 \times 64$ 维形状令牌）一同输入图 Transformer，使网络能同时感知几何干涉和形状先验。

### 多引导框架

在推理阶段，SPREAD 通过组合引导信号调节逆向扩散的得分函数：

$$
\nabla_{\mathbf{x_t}} \log p_\gamma(\mathbf{x_t}) = s_\theta(\mathbf{x_t}, t) + \gamma \nabla_{\mathbf{x_t}} \mathcal{G}(\mathbf{x_t})
$$

总引导 $\mathcal{G}$ 由三项加权组合：

$$
\mathcal{G} = \lambda_C \mathcal{G}_C + \lambda_H \mathcal{G}_H + \lambda_R \mathcal{G}_R
$$

其中权重配置为 $\lambda_C=7.5\times10^{-3}$，$\lambda_H=1\times10^{-3}$，$\lambda_R=1\times10^{-3}$。

**碰撞引导** $\mathcal{G}_C$ 基于锥形距离场（CoDF），对网格三角形对进行相交检测并施加可微惩罚：

$$
\mathcal{G}_C = \frac{1}{|C|} \sum_{a,b,a\neq b} \sum_{(i,j)\in C} \mathbf{CoDF}(t_a^i, t_b^j)
$$

**重力引导** $\mathcal{G}_H$ 惩罚物体悬浮或穿透地面的情况：

$$
\mathcal{G}_H = \sum_{r_i > \theta_H \lor r_i < 0} |r_i|
$$

其中 $\theta_H$ 为容忍高度阈值，超出该高度或低于地面的物体将被惩罚。

**关系引导** $\mathcal{G}_R$ 针对支撑关系，计算被支撑物体位于支撑体外的顶点到支撑凸包的最小欧氏距离，并按顶点数和关系数归一化：

$$
\mathcal{G}_R = \sum_{(i,j)\in E} \sum_{\alpha \in V_{i,j}} \frac{\mathbf{s}(\alpha,j)}{|V_{i,j}| |E|}
$$

其中 $E$ 为有向支撑边集合，$V_{i,j}$ 为物体 $i$ 位于支撑体 $j$ 外部的顶点集，$\mathbf{s}(\alpha,j)$ 为顶点 $\alpha$ 到支撑凸包的距离。这一引导显式地迫使被支撑物体精确放置于支撑面上，是降低平均支撑距离（ASD）的关键机制。

### 补充图表

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/008_Figure_5.jpg]]
*Figure 5: Guidance Ablation. Results showing effect of different guidance terms. Each major row compares results before (top) and after (bottom) adding a specific guidance. Columns show different scenes. Red circles highlight issues such as collisions, floating, or incorrect spatial relations before guidance; green circles show improvements after applying guidance, with zoom-in views for clarity*

## 实验与分析

### 主要结果

SPREAD 在两个差异显著的数据集——3D-FRONT（家具级室内场景）和 ProcTHOR-10K（细粒度物体交互场景）上进行了全面评估。实验结果表明，SPREAD 在物理合理性指标上全面超越现有方法，同时在视觉质量上保持竞争力。

**Table 1** 展示了定量对比的核心结论。在 3D-FRONT 数据集上，SPREAD 的 FID 与基线方法持平，但在网格碰撞率（Col_mesh）上取得了显著优势：卧室场景从 ATISS 的 0.275 降至 0.097，客厅场景从 InstructScene 的 0.350 降至 0.185，餐厅场景从 InstructScene 的 0.331 降至 0.183。

在 ProcTHOR 数据集上，SPREAD 建立了新的最优水平。关键指标包括：

- **图召回率（GRecall）**：0.979，优于 InstructScene 的 0.964，表明 SPREAD 对空间和物理关系的还原能力最强。
- **网格碰撞率（Col_mesh）**：0.121，较 InstructScene 的 0.260 降低了 53.5%，这归因于网格级碰撞引导的显式约束。
- **平均支撑距离（ASD）**：0.007，远低于 InstructScene 的 0.021，说明物体间支撑关系更精确，物体能更紧密地放置在支撑面上。
- **物理仿真稳定性（Isaac Stability）**：0.950，优于 InstructScene 的 0.876，表明生成的场景在 Isaac Sim 中经物理仿真后崩溃最少。
- **FID**：18.8，略优于 InstructScene 的 20.0，说明物理约束的引入并未损害视觉质量。

用户调研（**Figure 6**）进一步验证了主观层面的优势：SPREAD 以 88.6% 的得票率显著领先，ATISS 仅获 0.9%，InstructScene 获 4.4%，DiffuScene 获 6.1%。参与者被要求比较生成场景在物理仿真前后的物理一致性和场景合理性，SPREAD 的表现获得了压倒性认可。

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/009_Figure_6.jpg]]
*Figure 6: User Study. Our method dominated with 88.6% of the votes, above ATISS with 0.9%, InstructScene with 4.4%, and DiffuScene with 6.1%, indicating that our method better preserves physical consistency and scene rationality*

### 消融实验

**Table 2** 展示了在 ProcTHOR 上的消融结果，从基础模型（Base）开始逐步叠加组件：

- **Base 模型**：GRecall 0.963，Col_mesh 0.241，ASD 0.014，Stability 0.934。
- **+ 几何感知模块（Geometry Module）**：GRecall 提升至 0.965，Col_mesh 降至 0.225，ASD 降至 0.012，Stability 升至 0.938。几何感知器通过有向 Chamfer 距离捕捉网格级穿透信息，直接改善了碰撞和支撑精度。
- **+ 完整多引导框架（Multi-Guidance）**：所有指标达到最优——GRecall 0.979，Col_mesh 0.121，ASD 0.007，Stability 0.950。碰撞引导（λ_C=7.5e-3）、重力引导（λ_H=1e-3）和关系引导（λ_R=1e-3）的联合作用，使物理合理性得到全面提升。

**Figure 5** 提供了引导消融的可视化证据。每一行对比了添加特定引导前后的场景：碰撞引导消除了物体间的穿透（红圈标注的穿透区域变为绿色），重力引导纠正了悬浮物体，关系引导修复了不正确的空间布局。这些定性结果与定量指标相互印证。

此外，Michelangelo 形状编码器的使用对网格碰撞率有适度改善（Section 9），感知器 Transformer 相比普通 Transformer 在相同性能下计算成本更低、网络更浅。

### 推理效率

**Table 3** 对比了不同方法的推理时间。SPREAD 单场景推理约需 14.72 秒，虽然慢于 ATISS 等自回归方法，但考虑到其引入了网格级碰撞检测和多引导优化，这一开销是可接受的。实时应用场景仍存在优化空间。

### 失败模式与局限性

尽管 SPREAD 在物理合理性上取得了显著进步，仍存在以下局限：

1. **旋转参数化歧义**：扩散过程在欧氏空间中对旋转进行参数化，而非直接作用于 SE(3) 流形，可能引入旋转表示的不稳定性。
2. **场景类型受限**：当前模型仅针对室内场景设计和训练，室外无界场景的生成有待拓展。
3. **数据分布偏差**：ProcTHOR-10K 数据集由程序化生成（**Table 4** 展示了数据集统计），虽经预处理增强了关系复杂性（**Figure 7**），但仍可能无法完全代表真实世界的物体交互模式。
4. **FID 指标的局限性**：FID 主要评估视觉质量分布，无法充分反映物理合理性。SPREAD 在 FID 上与基线相当或略优，但可能以牺牲一定视觉多样性为代价换取物理鲁棒性，这一权衡需要根据下游任务需求审慎评估。
5. **用户调研样本量**：用户调研虽采用盲评和缩放功能减少偏差，但有效回复仅 57 份，结论的统计推广性需谨慎对待。

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/010_Table_4.jpg]]
*Table 4: Dataset Statistics. Summary of the processed ProcTHOR-10K dataset, detailing the scale of rooms, splits, and object diversity*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of relational complexity between our pre-processed dataset (left) and the original 3D-FRONT dataset (right). The sample from our dataset (left) contains a richer variety of indoor objects and exhibits complex, fine-grained spatial-physical relationships. In contrast, the sample from 3D-FRONT (right) lacks such fine-grained object interactions, particularly with small objects, highlighting the relational sparsity inherent in the original dataset that our preprocessing pipeline aims to address*

### 补充图表

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison. Our method matches baseline FID on 3D-FRONT while setting new state-of-the-art on ProcTHOR: it dramatically reduces mesh collisions, achieves the highest graph recall (GRecall), minimizes average support distance (ASD), and delivers the greatest scene stability under Isaac Sim*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/006_Table_2.jpg]]
*Table 2: Ablation on ProcTHOR. starting from our base model, adding the geometry module and then the full multi-guidance framework yields consistent improvements in all physical metrics*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/004_Figure_3.jpg]]
*Figure 3: Comparative Generation and Simulation Results. Visual comparison of scene layouts produced by our method versus three baseline approaches, shown before (left) and after (right) physics simulation*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/005_Figure_4.jpg]]
*Figure 4: Scene & Relation Visualization. For two generated scenes, we show the final render (left), the top-down layout (middle), and the pairwise relation evaluation matrix (right). The matrix encodes every object-pair’s spatial relation: green entries denote correct relations (w.r.t. the ground truth), and red entries denote incorrect ones*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/007_Table_3.jpg]]
*Table 3: Comparison of inference times (in seconds) across different scene generation methods*

![[assets/figures/papers/paper_list_l2601_https_arxiv_org_abs_2603_27573/figures/012_Figure_8.jpg]]
*Figure 8: Additional Qualitative results. The gallery displays 8 randomly selected samples, demonstrating the diversity and physical plausibility of the generated 3D scenes*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

SPREAD 针对现有 3D 场景生成方法在物理合理性上的系统性缺陷，提出了以可微分图先验和多引导框架为核心的解决方案。其核心差异体现在三个维度：

**与 ATISS 的对比：**
ATISS 采用自回归方式逐步添加物体，完全不考虑物理约束，导致场景中频繁出现物体悬浮和穿透。SPREAD 以扩散模型替代自回归范式，并引入图 Transformer 联合建模空间关系图 $\mathcal{G}_\rho$ 和物理关系图 $\mathcal{G}_\kappa$，从根本上将关系约束嵌入生成过程。在 ProcTHOR 数据集上，ATISS 的网格碰撞率高达 0.275，而 SPREAD 降至 0.121（见 Table 1）。

**与 DiffuScene 的对比：**
DiffuScene 虽同样基于扩散模型（使用 UNet-1D 和注意力机制），但其依赖形状码检索物体，缺乏对网格级几何状态的感知。SPREAD 在每个扩散时间步采样 M=2000 个表面点，计算有向 Chamfer 距离 $d_{\mathrm{scd}}$ 并通过感知器（Perceiver）提取几何感知特征，使模型能实时感知碰撞与穿透。此外，DiffuScene 无任何引导机制，而 SPREAD 的多引导框架（碰撞引导 $\mathcal{G}_C$、重力引导 $\mathcal{G}_H$、关系引导 $\mathcal{G}_R$）联合权重为 $7.5\times10^{-3}, 1\times10^{-3}, 1\times10^{-3}$，在推理时显式调节得分函数。

**与 InstructScene 的对比：**
InstructScene 采用两阶段框架（先学习语义图先验，再解码布局），虽在图召回率上表现较好（GRecall 0.964），但其依赖资产库检索，无法处理细粒度的物理交互。SPREAD 以端到端方式将图先验作为扩散图块的偏置输入，并通过图注意力沿显式边传播空间/物理关系，在 ProcTHOR 上将图召回率进一步提升至 0.979，同时将平均支撑距离（ASD）从 0.021 降至 0.007，物理仿真稳定性从 0.876 提升至 0.950（见 Table 1）。

### 2. 适用边界

SPREAD 的设计和验证集中在以下边界内：

- **场景类型：** 当前模型仅针对室内场景（卧室、客厅、餐厅）设计，训练和评估均在 3D-FRONT 和 ProcTHOR-10K 数据集上进行。室外无界场景的生成尚未探索。
- **物体交互：** 模型显式建模的空间关系（如“左侧”、“上方”）和物理关系（如“支撑”）限于预定义的离散类别。对于动态交互（如物体运动轨迹、时序一致性）未做建模。
- **旋转参数化：** 扩散过程在欧氏空间中对旋转进行参数化（6D 连续表示），而非直接在 SE(3) 流形上操作，可能引入旋转歧义。
- **数据依赖：** ProcTHOR 数据集虽经预处理增强了关系复杂性，但其原始数据由程序化生成，可能无法完全代表真实世界的物体多样性和场景复杂性。
- **推理效率：** 单场景推理约需 14.72 秒（见 Table 3），实时应用存在挑战。

### 3. 局限与开放问题

**已知局限：**
1. **场景泛化：** 模型仅在室内家具布局上验证，扩展到室外场景需要重新定义空间/物理关系类别和引导函数。
2. **旋转建模：** 欧氏空间中的旋转参数化可能导致生成结果在物理仿真中出现不自然的旋转偏移，直接在 SE(3) 流形上进行扩散是潜在的改进方向。
3. **计算开销：** 每个去噪步需采样表面点并计算有向 Chamfer 距离，加上多引导框架的梯度计算，推理时间显著高于 ATISS 等轻量方法。
4. **引导权重调优：** 多引导框架中三项引导的权重（$\lambda_C, \lambda_H, \lambda_R$）目前通过实验手动设定，缺乏自动调优策略。
5. **评估指标局限：** FID 等视觉质量指标无法完全反映物理合理性，对物理任务的评估仍需依赖 Col_mesh、ASD、Stability 等专门指标，且用户调研样本量有限（57 份有效回复），主观结论需谨慎推广。

**开放问题：**
- 如何将 SPREAD 的图先验和多引导框架扩展到室外无界场景？
- 能否通过蒸馏或一步生成方法减少迭代扩散过程的计算开销？
- 如何在 SE(3) 流形上直接进行扩散，以更好地处理旋转并避免歧义？
- 如何处理动态场景中的时间一致性和物体运动轨迹生成？
- 多引导框架中各项引导权重的自动调优策略（如基于强化学习或元学习）是否可行？
- 如何将物理仿真反馈直接纳入训练循环，形成闭环优化？

## 原文 PDF

![[paperPDFs/CVPR_2026/SPREAD_Spatial_Physical_REasoning_via_geometry_Aware_Diffusion.pdf]]