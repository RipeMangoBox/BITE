---
title: "SimScale: Learning to Drive via Real-World Simulation at Scale"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SimScale_Learning_to_Drive_via_Real_World_Simulation_at_Scale.pdf
project_link: "https://opendrivelab.com/SimScale"
code_link: "https://github.com/OpenDriveLab/SimScale"
aliases:
- SimScale
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 仿真数据规模、伪专家监督模式（恢复型 vs. 规划器型）以及反应式环境模拟。
primary_logic: 通过高保真3DGS仿真大规模生成OOD状态，结合伪专家演示或奖励信号进行sim-real协同训练，不仅可以有效弥补真实数据多样性不足，而且能在不增加真实数据的情况下，使多种规划器的鲁棒性和泛化性获得可预测的持续提升。
claims:
- 在navhard评测中，基于奖励信号训练的GTRS-Dense (ResNet34) EPDMS从38.3提升至46.9 (+8.6)。
- 在navtest评测中，LTF规划器的EPDMS从81.5提升至84.4 (+2.9)。
- 增加仿真数据规模，规划性能遵循对数二次曲线平滑增长，无早期饱和迹象。
- 反应式仿真相比非反应式仿真在GTRS-Dense上带来约+2.3 EPDMS的持续提升。
---

# SimScale: Learning to Drive via Real-World Simulation at Scale

> [!tip] 核心洞察
> 通过高保真3DGS仿真大规模生成OOD状态，结合伪专家演示或奖励信号进行sim-real协同训练，不仅可以有效弥补真实数据多样性不足，而且能在不增加真实数据的情况下，使多种规划器的鲁棒性和泛化性获得可预测的持续提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | SimScale：通过大规模真实世界仿真学习驾驶 |
| 英文题名 | SimScale: Learning to Drive via Real-World Simulation at Scale |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.23369) · [Project](https://opendrivelab.com/SimScale) · [Code](https://github.com/OpenDriveLab/SimScale) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SimScale |
| Dataset | NAVSIM-v2 navhard, NAVSIM-v2 navtest |

> [!tip] 效果简介
> - NAVSIM-v2 navhard 上，EPDMS GTRS-Dense (ResNet34) + SimScale (reward-only) vs GTRS-Dense (ResNet34) w/o sim (+8.6 (38.3 -> 46.9))；EPDMS DiffusionDrive + SimScale vs DiffusionDrive w/o sim (+5.1 (27.5 -> 32.6))；EPDMS GTRS-Dense (V2-99) + SimScale (reward-only) vs GTRS-Dense (V2-99) w/o sim (+6.1 (41.9 -> 48.0))。
> - NAVSIM-v2 navtest 上，EPDMS LTF + SimScale vs LTF w/o sim (+2.9 (81.5 -> 84.4))。

## 概要

真实世界驾驶数据中安全关键和分布外（OOD）场景严重不足，导致端到端规划器在未见过情境下泛化性差。**SimScale** 针对这一瓶颈，提出通过高保真3D高斯泼溅（3DGS）仿真大规模生成OOD状态，并结合伪专家演示或奖励信号进行sim-real协同训练，从而在不增加真实数据的前提下，使多种规划器的鲁棒性和泛化性获得可预测的持续提升。

核心方法包括三条因果链路：（1）**仿真数据规模**——从真实数据重建静态背景与可移动车辆资产，通过对人类历史轨迹进行可控扰动覆盖OOD状态，经反应式环境模拟（LQR自车 + IDM他车）渲染多视图观测；（2）**伪专家监督模式**——提供恢复型（保守回退）与规划器型（探索性优化）两种伪专家轨迹，对评分型规划器甚至可仅用仿真奖励信号；（3）**sim-real协同训练**——混合真实与仿真数据联合训练，保持人类驾驶分布的同时引入OOD知识。

在NAVSIM-v2基准上，SimScale展现出跨规划器架构的通用增益：**navhard**评测中，GTRS-Dense (ResNet34) 的EPDMS从38.3提升至46.9（+8.6），DiffusionDrive从27.5提升至32.6（+5.1）；**navtest**评测中，LTF规划器从81.5提升至84.4（+2.9）。消融实验进一步揭示：规划器型伪专家优于恢复型伪专家，反应式仿真相比非反应式仿真带来约+2.3 EPDMS的持续提升，且规划性能随仿真数据规模遵循对数二次曲线平滑增长，未出现早期饱和迹象。

SimScale的定位是**仿真驱动的端到端规划扩展框架**，其方法谱系可归纳为：以3DGS重建为数据引擎，以轨迹扰动与伪专家生成为知识扩展手段，以反应式环境模拟为逼真度保障，以sim-real协同训练为学习范式。相较于仅依赖真实数据或静态仿真的既有方案，SimScale首次系统验证了仿真数据规模、监督信号类型与环境交互性对规划器性能的联合缩放效应，为端到端自动驾驶的仿真扩展提供了可复现的基准与开放工具链。



端到端自动驾驶系统近年来取得了显著进展，但其在真实世界中的鲁棒性和泛化性仍面临根本性瓶颈：**安全关键（safety-critical）和分布外（OOD）场景在真实驾驶数据中严重不足**。现有真实世界驾驶数据集主要捕获常规、安全的驾驶行为，极少覆盖需要紧急避障、异常交互或极端交通条件的边缘情形。这种数据分布的长尾特性直接导致端到端规划器在未见过情境下性能急剧退化——规划器在训练分布内的表现良好，但一旦遭遇偏离训练统计的OOD状态，往往输出不安全或不可行的轨迹。

这一瓶颈的深层原因在于**真实数据采集的成本与覆盖范围之间存在不可调和的矛盾**。真实道路测试或众包采集受限于安全约束、地理覆盖和场景自然发生率：高危场景本身稀有，且无法在真实环境中主动制造。因此，仅依赖真实数据的端到端系统天然存在泛化天花板，单纯增加真实数据量的边际收益递减且难以覆盖长尾。

现有应对策略可大致归为两类。一类是**基于规则或符号输入的规划器**（如PDM-Closed），它们利用真值感知信息进行规划，在已知场景中表现稳健，但缺乏对传感器噪声和感知误差的容错能力，且无法从数据中学习更优的驾驶策略。另一类是**基于学习的端到端规划器**，包括回归型（如**LTF**）、扩散型（如**DiffusionDrive**）和评分型（如**GTRS-Dense**）等代表性范式。这些方法虽然展现了从传感器输入直接输出规划轨迹的能力，但它们的性能上限严重受限于训练数据的场景多样性。当面对训练集中未充分覆盖的OOD状态时，这些规划器缺乏足够的监督信号来学习正确的应对策略。

**仿真**为突破上述数据瓶颈提供了潜在路径。然而，现有仿真方法存在两个关键缺口：其一，传统仿真器（如基于游戏引擎的方案）虽能生成多样化场景，但其视觉渲染与真实世界存在显著的领域差异（sim-real gap），导致仿真训练的模型难以迁移到真实环境；其二，仿真中通常缺乏与真实人类驾驶分布对齐的**可行专家轨迹**，使得仿真数据无法直接提供有效的模仿学习监督信号。

SimScale正是在这一背景下提出的。其核心动机是：**能否利用真实世界数据本身构建高保真仿真，从已有专家分布中扩展出大规模OOD状态及其对应的可行解决方案，从而在不增加真实数据采集成本的前提下，系统性地提升端到端规划器的鲁棒性和泛化性？** 这一思路的关键洞察在于，真实数据中蕴含的驾驶知识和场景结构可以通过3D高斯泼溅（3DGS）重建和轨迹扰动被“解耦-重组-扩展”，生成既保持视觉逼真度又覆盖OOD状态的新训练样本。更重要的是，这种仿真数据生成可以规模化——随着仿真数据量的增加，多种范式规划器的性能呈现出可预测的持续提升趋势，而非早期饱和，这暗示着一条通过仿真扩展实现端到端驾驶能力持续增长的可行路径。



## 核心方法与创新机理

SimScale 的核心创新并非提出一种新的规划器架构，而是构建了一套**与规划器解耦的大规模仿真数据生成与协同训练系统**，通过三个关键“改变槽”（changed slots）系统性地解决了端到端驾驶中安全关键和分布外（OOD）场景严重不足的根本瓶颈。

### 从真实数据到仿真数据的训练数据源扩展

传统端到端规划器仅依赖真实世界的导航训练集（navtrain）进行模仿学习，数据中安全关键场景天然稀疏，导致模型在未见过情境下泛化性差。SimScale 的核心突破在于**将训练数据源从“仅真实数据”扩展为“真实数据 + 大规模 3DGS 仿真数据”**。这一扩展并非简单的数据增强，而是通过以下机制实现对 OOD 状态的系统性覆盖：

1. **轨迹扰动**：对人类历史轨迹进行可控扰动，生成偏离专家分布的 OOD 自车状态，并通过空间稀疏采样过滤不可行轨迹。
2. **反应式环境模拟**：在仿真中让周围代理与自车行为交互（LQR 自车控制器 + IDM 他车模型），使场景动态响应自车的异常行为，而非静态回放。
3. **3DGS 视觉渲染**：从真实数据重建的静态背景与可移动车辆资产中渲染新视角多视图观测，为扰动后的场景提供对应的传感器输入。

这种数据生成管线使得仿真数据能够覆盖真实数据中几乎不出现的长尾状态，为规划器提供了接触 OOD 场景的训练机会。

### 从人类专家轨迹到伪专家监督信号的转变

传统方法仅使用人类专家轨迹作为监督信号，但在仿真生成的 OOD 状态下，人类轨迹不可得。SimScale 引入了**两种互补的伪专家轨迹生成策略**，将监督信号从“仅人类专家”扩展为“伪专家轨迹或奖励信号”：

- **恢复型伪专家**：通过匹配向量 $\mathbf{m} = [\tilde{v}_t^x, \tilde{v}_t^y, \tilde{\theta}_t, \tilde{x}_{t+H-1}, \tilde{y}_{t+H-1}, \tilde{\theta}_{t+H-1}]$ 从人类轨迹词汇表 $\mathcal{V}_h$ 中检索最接近的轨迹 $\tilde{a}_{t:t+H} = \arg\min_{a\in\mathcal{V}_h} \|\mathbf{m}(a) - \mathbf{m}_r\|_1$，生成类人但保守的回退行为。这种方式约束较强，数据积累速度较慢，但稳定性好。
- **规划器型伪专家**：使用特权规划器（PDM-Closed）在 OOD 状态下进行反应式轨迹优化 $\tilde{a}_{t:t+H} = \mathbf{P}(\tilde{s}_{t:t+H})$，生成更具探索性的行为。这种方式数据积累效率更高，且在不同规划器上展现出更好的扩展趋势。
- **仅奖励信号**：对于评分型规划器（如 GTRS-Dense），SimScale 发现仅使用仿真环境中的奖励评分即可达到甚至超越使用专家轨迹的效果——这揭示了在仿真环境中，奖励信号本身已足够提供有效的学习指导。

### 从非反应式到反应式仿真动力学的升级

传统仿真通常采用静态环境（非反应式），即周围代理行为不受自车动作影响。SimScale 将仿真动力学从“非反应式”升级为“反应式”，通过 LQR 控制自车轨迹、IDM 模型驱动他车交互，使仿真场景具有因果闭环特性。消融实验表明，反应式仿真相比非反应式仿真在 GTRS-Dense 上带来约 **+2.3 EPDMS** 的持续提升，而非反应式仿真几乎不带来性能增益——这证明反应式环境模拟是发挥仿真数据潜力的关键使能因素。

### 仿真扩展律的发现

SimScale 的另一重要创新是**首次揭示了端到端规划器性能随仿真数据规模的对数二次扩展律** $S(N) = a \log^2(N) + b \log(N) + c$。实验表明，增加仿真数据规模，规划性能遵循该曲线平滑增长，无早期饱和迹象，这为仿真驱动的自动驾驶系统规模化训练提供了可预测的理论指导。

### 与基线方法的本质区别

上述三个 changed slots 共同构成了 SimScale 与现有工作的本质区别：它不是改进规划器本身，而是**构建了一个通用的仿真数据基础设施**，使得回归型（LTF）、扩散型（DiffusionDrive）、评分型（GTRS-Dense）等不同家族的规划器均能通过 sim-real 协同训练获得一致的鲁棒性和泛化性提升。这种“规划器无关”的特性是 SimScale 作为方法框架的核心竞争力。



SimScale 构建了一套完整的“仿真数据生成—伪专家监督—协同训练”闭环系统，旨在以可扩展的方式弥补真实世界驾驶数据中安全关键与分布外（OOD）场景的不足。其核心洞察在于：通过高保真 3DGS 仿真大规模生成 OOD 状态，结合伪专家演示或奖励信号进行 sim-real 协同训练，可以在不增加真实数据的前提下，使多种端到端规划器的鲁棒性与泛化性获得可预测的持续提升。

### 系统总览

整个 SimScale 系统由两大核心组件构成：**可扩展的仿真数据构造管线**与**sim-real 协同训练策略**（Figure 1）。前者负责从真实数据中重建可操作的 3D 场景，并通过轨迹扰动与反应式模拟生成覆盖广泛 OOD 状态的多视图观测及对应监督信号；后者将仿真数据与真实导航训练数据混合，对任意端到端规划器进行联合训练，使模型在保持人类驾驶分布的同时习得处理罕见情形的能力。

### 管线模块与数据流

SimScale 的仿真数据生成管线包含四个关键模块，数据流依次经过：

1. **3DGS 数据引擎（3DGS Data Engine）**  
   从真实世界数据集重建 3DGS 资产，采用分块重建策略将场景解耦为静态背景与可移动车辆前景。给定相机内参 $K_t$、外参 $E_t$ 以及非自车代理的位置与朝向 $\{x_{i,t}, y_{i,t}, \theta_{i,t}\}_{i=1}^N$，引擎渲染对应的多视图 RGB 观测：
   $$\Phi(K_t, E_t, \{x_{i,t}, y_{i,t}, \theta_{i,t}\}_{i=1}^N)$$
   这一解耦设计使得后续仿真可以独立操控自车与他车的行为，而无需重新渲染全局场景。

2. **轨迹扰动（Trajectory Perturbation）**  
   在时间窗口 $[T, T+H]$ 上对人类历史轨迹施加可控扰动，生成偏离专家分布的 OOD 状态。扰动后的轨迹经过空间稀疏采样过滤，剔除不可行轨迹（如碰撞、偏离道路），确保后续伪专家生成的有效性。

3. **反应式环境模拟（Reactive Environment Simulation）**  
   行为模拟与传感器渲染解耦：自车轨迹 $\tilde{a}_{t:t+H}$ 通过 LQR 控制器执行，周围代理则采用 IDM 模型与自车行为交互。这种反应式设计相比非反应式（静态环境）仿真，能显著增强场景的逼真度与多样性，是发挥仿真数据潜力的关键前提（Table 4 显示反应式仿真带来约 +2.3 EPDMS 的持续提升）。

4. **伪专家轨迹生成（Pseudo-Expert Trajectory Generation）**  
   从 OOD 状态 $\tilde{s}_{t:t+H}$ 出发，生成时间窗口 $[T+H, T+2H]$ 上的可行伪专家轨迹，提供行动监督。系统支持两种策略：
   - **恢复型专家（Recovery-based）**：通过匹配向量 $\mathbf{m} = [\tilde{v}_t^x, \tilde{v}_t^y, \tilde{\theta}_t, \tilde{x}_{t+H-1}, \tilde{y}_{t+H-1}, \tilde{\theta}_{t+H-1}]$ 在人类轨迹词汇表 $\mathcal{V}_h$ 中检索最接近的轨迹：
     $$\tilde{a}_{t:t+H} = \arg\min_{a\in\mathcal{V}_h} \|\mathbf{m}(a) - \mathbf{m}_r\|_1$$
     该策略产生保守、类人的回退行为，稳定性强但数据积累较慢。
   - **规划器型专家（Planner-based）**：使用特权规划器 $\mathbf{P}$ 直接生成反应式优化轨迹：
     $$\tilde{a}_{t:t+H} = \mathbf{P}(\tilde{s}_{t:t+H})$$
     该策略探索性更强，数据积累效率更高，且在多种规划器上展现出更优的扩展趋势。

### 协同训练框架

仿真数据生成后，与真实导航训练集 $\mathcal{D}$ 混合形成联合数据集 $\mathcal{D} \cup \mathcal{D}_{sim}$。对于以模仿学习为主的规划器（如 LTF、DiffusionDrive），协同训练目标为最小化联合数据上的模仿损失：
$$\arg\min_\theta \mathbb{E}_{(a,o)\sim(\mathcal{D}\cup\mathcal{D}_{sim})}[\mathcal{L}_{im}(a,\pi_\theta(\hat{a}|o))]$$
对于评分型规划器（如 GTRS-Dense），仿真数据中可直接使用奖励信号 $\mathcal{L}_r$ 替代专家轨迹，实现“奖励即一切”（Reward is All You Need）的训练范式。所有模型采用统一的训练协议：从头训练，输入分辨率固定为 $2048 \times 512$，移除 LiDAR 输入以对齐 navhard 评测设置。

### 输入输出规范

- **输入**：多视图 RGB 图像（分辨率 $2048 \times 512$），来自真实数据或 3DGS 渲染的仿真观测。
- **输出**：自车未来 $H$ 步的轨迹规划 $\hat{a}_{t:t+H}$。
- **监督信号**：真实数据使用人类专家轨迹；仿真数据使用伪专家轨迹（恢复型/规划器型）或仅奖励评分（针对评分型规划器）。



SimScale 的仿真-真实协同学习系统由四个关键模块串联构成：**3DGS 数据引擎**、**轨迹扰动与伪专家生成**、**反应式环境模拟**以及**Sim-Real 协同训练**。本节聚焦各模块的核心机制与关键公式。

### 3DGS 数据引擎

数据引擎建立在从真实世界数据集重建的 3DGS 资产之上。通过逐时间步的 3D 边界框位置与朝向，将场景分解为**静态背景资产**与**可移动车辆资产**，实现背景与前景的分离重建。渲染函数形式化为：

$$\Phi(K_t, E_t, \{x_{i,t}, y_{i,t}, \theta_{i,t}\}_{i=1}^{N})$$

其中 $K_t$ 为相机内参，$E_t$ 为外参，$\{x_{i,t}, y_{i,t}, \theta_{i,t}\}$ 表示第 $i$ 个非自车代理在时间步 $t$ 的位置与偏航角。该引擎支持对自车和其他代理状态的时序控制，并从自车视角渲染多视图 RGB 观测。

### 轨迹扰动与伪专家生成

**轨迹扰动**：对人类历史轨迹施加可控扰动以覆盖 OOD 状态。扰动后的轨迹通过空间稀疏采样过滤不可行路径，确保生成的初始状态 $\tilde{s}_t$ 在物理上可达。

**恢复型伪专家**（Recovery-based Expert）：从人类轨迹词汇表 $\mathcal{V}_h$ 中检索最匹配的轨迹作为伪专家动作。首先构造紧凑匹配向量：

$$\mathbf{m} = [\tilde{v}_t^x, \tilde{v}_t^y, \tilde{\theta}_t, \tilde{x}_{t+H-1}, \tilde{y}_{t+H-1}, \tilde{\theta}_{t+H-1}]$$

该向量概括候选轨迹的初始速度分量、初始偏航角以及终点位姿。随后通过最小化 L1 距离完成检索：

$$\tilde{a}_{t:t+H} = \arg\min_{a \in \mathcal{V}_h} \|\mathbf{m}(a) - \mathbf{m}_r\|_1$$

其中 $\mathbf{m}_r$ 为目标匹配向量。恢复型专家产生类人但保守的回退行为，在分布漂移下具有稳定化作用。

**规划器型伪专家**（Planner-based Expert）：使用特权规划器 $\mathbf{P}$（基于规则的 PDM-Closed）从扰动状态序列直接生成反应式优化轨迹：

$$\tilde{a}_{t:t+H} = \mathbf{P}(\tilde{s}_{t:t+H})$$

相比恢复型专家，规划器型专家生成的动作更具探索性，数据积累效率更高（见图 3）。

### 反应式环境模拟

仿真中将行为模拟与传感器渲染解耦。自车轨迹 $\tilde{a}_{t:t+H}$ 通过 **LQR** 控制器执行，其他代理采用 **IDM** 跟驰模型与自车交互。这种反应式设计使仿真环境能够响应自车行为变化，显著提升场景逼真度与训练数据的有效性（消融实验证实，非反应式仿真几乎不带来性能增益，见 Table 4）。

### Sim-Real 协同训练

协同训练目标在真实数据 $\mathcal{D}$ 与仿真数据 $\mathcal{D}_{sim}$ 上联合优化。对于基于模仿学习的规划器（如 LTF、DiffusionDrive），目标为：

$$\arg\min_\theta \mathbb{E}_{(a,o) \sim (\mathcal{D} \cup \mathcal{D}_{sim})}[\mathcal{L}_{im}(a, \pi_\theta(\hat{a}|o))]$$

其中 $a$ 为专家动作（真实数据使用人类轨迹，仿真数据使用伪专家轨迹），$o$ 为观测，$\pi_\theta$ 为规划器策略。对于评分型规划器 GTRS-Dense，仿真数据可直接使用环境奖励信号 $\mathcal{L}_r$ 替代专家轨迹监督，实现“奖励即一切”的训练范式。

### 扩展律公式

实验发现规划性能 $S(N)$ 与总数据规模 $N$ 之间遵循对数二次关系：

$$S(N) = a \log^2(N) + b \log(N) + c$$

该扩展律在多种规划器家族上均成立，表明仿真数据带来的性能提升具有可预测的平滑增长趋势，未出现早期饱和迹象。

### 补充图表

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/002_Figure_2.jpg]]
*Figure 2: Pseudo-expert scene simulation pipeline. (a) Trajectory perturbation on T to T + H, (b) reactive environment rollout, and pseudo-expert trajectory generation from T + H to T + 2H under recovery-based and planner-based strategies*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/003_Figure_3.jpg]]
*Figure 3: Simulation data statistics across multiple sampling rounds. (a) Recovery-based expert impose stronger constraints, leading to slower data accumulation than (b) Planner-based expert*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/011_Figure_6.jpg]]
*Figure 6: Learning paradigm comparison of e2e autonomous driving between 3DGS-based Online RL and SimScale*



## 实验与关键发现

### 核心实验设置

SimScale 的实验评估基于 **NAVSIM‑v2** 基准的两个官方评测集：**navhard**（高难度安全关键场景）和 **navtest**（标准测试集）。所有模型均从零训练，统一输入分辨率为 $2048 \times 512$，移除 LiDAR 输入以对齐 navhard 评测协议。真实训练数据固定为 navtrain 划分，仿真数据通过非重叠采样逐步累加，以独立评估仿真扩展效应。训练硬件为 NVIDIA H20‑3e GPU，所有方法采用相同的训练策略以保证公平对比。

评测指标采用 **EPDMS**（Expected Penalized Driving Model Score），其定义为惩罚项乘积与加权平均项的组合：

$$\mathrm{EPDMS} = \left(\prod_{m\in\mathcal{M}_{pen}} S_m\right) \cdot \left(\frac{\sum_{m\in\mathcal{M}_{avg}} w_m S_m}{\sum_{m\in\mathcal{M}_{avg}} w_m}\right)$$

该指标综合了碰撞、越界、不舒适等惩罚子项与速度保持、横向位置等加权子项，能够较全面地反映规划器在安全性与驾驶质量之间的权衡。仿真数据生成管线的具体配置见 **Table 5**，模型与训练超参数见 **Table 6**。

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/010_Table_5.jpg]]
*Table 5: Simulation Data Curation Pipeline Configurations*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/012_Table_6.jpg]]
*Table 6: Model and Training Hyperparameters*

### 主要结果：Sim‑Real 协同训练带来跨架构一致提升

**Table 1** 展示了 navhard 榜单上的主要结果。在三种结构迥异的端到端规划器上，引入 SimScale 仿真数据均带来显著且一致的性能增益：

- **回归型规划器 LTF**：EPDMS 从 24.4 提升至 30.2（+5.8，相对提升约 24%）。
- **扩散型规划器 DiffusionDrive**：EPDMS 从 27.5 提升至 32.6（+5.1，相对提升约 19%）。
- **评分型规划器 GTRS‑Dense (ResNet34)**：使用仅奖励信号（reward‑only）训练时，EPDMS 从 38.3 提升至 **46.9**（**+8.6**），达到所有传感器驱动方法中的最优水平。
- 当 GTRS‑Dense 升级到更强的 V2‑99 视觉骨干时，reward‑only SimScale 进一步将 EPDMS 从 41.9 推至 48.0（+6.1）。

在 navtest 标准测试集（**Table 2**）上，LTF 规划器在 SimScale 辅助下 EPDMS 从 81.5 提升至 84.4（+2.9），表明仿真数据不仅增强了安全关键场景的鲁棒性，也温和改善了常规场景下的驾驶质量。详细子指标分解见 **Table 7**（navhard）与 **Table 8**（navtest）。

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/005_Table_2.jpg]]
*Table 2: Performance on the NAVSIM-v2 navtest Leaderboard. (∗: pseudo-expert supervision; †: reward scoring.)*

值得注意的是，基于规则的特权规划器 **PDM‑Closed**（使用真值符号输入）在 navhard 上达到 58.7 EPDMS，为传感器驱动方法提供了性能上界参考。SimScale 使纯视觉规划器大幅缩小了与该上界的差距。

### 仿真数据扩展律：可预测的对数二次增长

**Figure 4** 揭示了仿真数据规模与规划器性能之间的扩展规律。随着仿真数据从零逐步增加，各规划器的 EPDMS 遵循平滑的对数二次曲线增长，未见早期饱和迹象。论文将这一关系形式化为扩展律：

$$S(N) = a \log^2(N) + b \log(N) + c$$

其中 $N$ 为总数据规模，$S(N)$ 为规划器性能。该规律表明，SimScale 框架下的仿真数据扩充具有可预测的收益递减特征——初始数据带来最大边际增益，但持续增加数据仍能稳定提升性能，为大规模部署提供了工程指导。

### 消融研究：伪专家类型、监督信号与环境反应性的关键作用

**伪专家类型与监督模式**（**Table 3**）：对于评分型规划器 GTRS‑Dense，仅使用仿真环境中的奖励信号（reward‑only）即可达到甚至超越使用伪专家轨迹的效果，验证了“奖励即一切”的论断。在伪专家轨迹监督中，**探索性规划器型专家**（planner‑based）在多种规划器上展现出优于**保守恢复型专家**（recovery‑based）的扩展趋势（**Figure 4**），因为前者生成的轨迹更接近最优解而非简单回退。两种专家的数据积累效率差异在 **Figure 3** 中量化：规划器型专家因约束更宽松，在相同采样轮次下积累的可行数据量更大。

**反应式环境模拟**（**Table 4**）：在 GTRS‑Dense 上，反应式仿真（LQR 自车 + IDM 他车）相比非反应式仿真（静态环境）带来约 **+2.3 EPDMS** 的持续提升。非反应式仿真几乎不带来性能增益，表明环境代理对自车行为的动态响应是仿真数据产生训练价值的关键前提。**Figure 7** 进一步展示了不同模型规模下反应式/非反应式仿真的扩展动态差异。

**视觉保真度**（**Table 10**）：提高仿真渲染质量（PSNR ≥ 27）有助于缩小 sim‑real gap，带来额外的性能增益。3DGS 重建质量不足的场景（PSNR < 27）被剔除，以确保仿真数据的视觉可靠性。

**多专家集成**（**Table 9**）：融合恢复型专家、规划器型专家与奖励型评分三种监督信号，可在单一专家基础上带来额外 +0.8 至 +2.9 EPDMS 的提升，表明不同监督模式存在互补性。

### 仿真数据分布特征与失效模式

**Figure 8** 分析了仿真数据与真实数据之间的分布偏移。EgoMLP 规划器在仿真数据上的 EPDMS 分布与真实数据存在系统性差异，按场景标签排序后揭示出仿真数据在特定场景类型（如交叉口、密集交通流）上的表现特征。这一分布偏移是 sim‑real gap 的重要来源，也是限制仿真训练增益完全迁移至真实环境的瓶颈。

**Figure 9** 展示了在固定 sim‑real 数据比例下，随真实数据规模变化的仿真扩展效果。结果表明仿真数据的增益在真实数据量较小时更为显著，而随着真实数据增加，额外仿真数据的边际收益递减但仍保持正向。

### 局限性与待验证问题

尽管 SimScale 在多项评测中展现出稳定的扩展能力，仍需注意以下限制：

1. **伪专家质量上限**：当前伪专家轨迹扰动基于规则，缺乏自进化能力；特权规划器 PDM‑Closed 本身性能有限（navhard EPDMS 58.7），在极端 corner case 中可能失效，导致舒适度指标（HC、EC）下降。
2. **交通模拟简化**：他车行为仅采用 IDM 模型，虽提供了基础交互，但限制了场景多样性。扩散式交通生成器可能是提升多样性的潜在方向，但尚未集成。
3. **传感器模拟局限**：前馈高斯泼溅的重建效率与视觉真实感仍有提升空间，仿真视觉伪影可能对部署到真实极端场景构成潜在风险。
4. **闭环自博弈缺失**：当前框架未引入自博弈（self‑play）等高级交互学习范式，闭环多代理协同演化尚未探索。

上述限制需要在实际部署前进行手动验证，尤其是仿真数据在真实极端场景下的迁移效果。

### 补充图表

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/004_Table_1.jpg]]
*Table 1: Performance on the NAVSIM-v2 navhard Leaderboard. PDM-Closed uses ground-truth symbolic inputs for planning, while other methods rely on sensor data. (∗: pseudo-expert supervision; †: reward scoring; S.: per-stage EPDM score.)*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/007_Figure_4.jpg]]
*Figure 4: Scaling dynamics across different planners and pseudo-expert trajectories. We visualize how simulation data scale and supervision signals influence the driving performance of various planners, where the infection point indicates learning plateau*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/008_Table_4.jpg]]
*Table 4: The effect between non-reactive vs. reactive data simulation on navhard using GTRS-Dense, across sampling rounds*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/009_Table_3.jpg]]
*Table 3: The effect of expert with simulated reward scoring on navhard using GTRS-Dense. (S1/2:per-stage EPDM scores.)*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/014_Figure_7.jpg]]
*Figure 7: Scaling dynamics under reactive and non-reactive simulation using GTRS-Dense across model sizes*

![[assets/figures/papers/paper_list_l2140_https_arxiv_org_abs_2511_23369/figures/015_Table_9.jpg]]
*Table 9: The effect of multi-expert ensemble on navhard using GTRS-Dense*



## 定位与知识库关联

### 1. 在端到端规划器谱系中的位置

SimScale 并非提出一种新的规划器架构，而是一种**数据生成与训练范式**，可即插即用地应用于三类代表性的端到端规划器家族：

- **回归型规划器**：**LTF**（直接回归未来轨迹点）。
- **扩散型规划器**：**DiffusionDrive**（通过去噪扩散过程生成轨迹）。
- **评分型规划器**：**GTRS-Dense**（从轨迹词汇表中检索并评分候选轨迹）。

SimScale 通过向这些规划器注入大规模仿真数据与伪专家监督（或奖励信号），在不修改模型架构的前提下，系统性地提升其在安全关键场景下的鲁棒性与泛化性。这种“数据驱动扩展”的定位使其区别于设计新型网络结构或损失函数的工作。

### 2. 与相关仿真/数据增强方法的边界

#### 2.1 与基于3DGS的在线强化学习（Online RL）的对比

论文明确将 SimScale 与基于 3DGS 的在线 RL 范式进行区分（见 **Figure 6**）。在线 RL 方法在仿真环境中通过试错探索学习策略，面临样本效率低、奖励设计困难以及 sim-real 迁移不稳定等问题。SimScale 则采用**离线协训练**策略：在仿真中生成 OOD 状态与伪专家轨迹，与真实数据混合后进行模仿学习或奖励评分训练，避免了在线交互的高成本与不稳定性。

#### 2.2 与纯真实数据训练（Real-Only）的对比

SimScale 的核心因果杠杆在于**仿真数据规模的扩展**。实验表明，仅使用真实导航训练集（navtrain）时，各类规划器在 navhard 评测上的表现均受限（如 GTRS-Dense 仅 38.3 EPDMS）。加入仿真数据后，性能遵循对数二次曲线平滑增长（见 Eq. 7-8），**无早期饱和迹象**，表明仿真数据有效弥补了真实数据中安全关键场景的不足。

#### 2.3 与特权规划器（Privileged Planner）的对比

SimScale 使用基于规则的 **PDM-Closed** 作为特权规划器生成伪专家轨迹。PDM-Closed 利用真值符号输入（ground-truth symbolic inputs）进行规划，在 navhard 上达到 45.5 EPDMS。SimScale 使传感器数据驱动的规划器（如 GTRS-Dense V2-99）达到 48.0 EPDMS，**超越了特权规划器的性能**，证明了仿真协训练的有效性。

### 3. 适用边界与关键依赖

SimScale 的有效性依赖于以下关键设计选择，偏离这些条件可能导致性能下降：

- **反应式环境模拟**：非反应式仿真（静态环境）几乎不带来性能提升（**Table 4**）。反应式仿真（LQR 自车 + IDM 他车）是发挥仿真数据潜力的必要条件，在 GTRS-Dense 上带来约 +2.3 EPDMS 的持续提升。
- **仿真视觉保真度**：3DGS 重建质量（PSNR ≥ 27）对减小 sim-real 差距至关重要（**Table 10**）。低质量渲染会引入视觉伪影，损害协训练效果。
- **伪专家质量**：探索性伪专家（规划器型）优于保守伪专家（恢复型），前者在多种规划器上展现出更好的扩展趋势（**Figure 4, Table 3**）。对于评分型规划器，仅使用仿真中的奖励信号即可达到甚至超越使用专家轨迹的效果（**Table 3**），表明奖励信号在仿真环境中已足够。
- **数据分布匹配**：仿真数据通过非重叠采样逐步累加，且协训练保持真实数据分布，避免灾难性遗忘。

### 4. 局限与开放问题

#### 4.1 已明确的局限

1. **伪专家生成的规则依赖**：当前轨迹扰动与伪专家生成基于规则（恢复型检索、基于 PDM-Closed 的规划器型），缺乏自进化能力，可能限制对更极端情形的覆盖。
2. **特权规划器的性能瓶颈**：PDM-Closed 作为特权规划器，性能有限，可能导致舒适度指标（HC、EC）下降，且在极端 corner case 中失效。
3. **交通行为模拟的多样性受限**：仅采用 IDM 模型控制他车行为，虽保证了交互可控性，但限制了场景多样性。
4. **传感器模拟效率**：仅使用前馈高斯泼溅，重建效率仍有提升空间。
5. **闭环多代理协同演化缺失**：尚未集成自博弈（self-play）等更高级的交互学习方式，无法实现多代理协同演化。
6. **sim-real gap 的残余风险**：协训练可能受仿真视觉不真实与分布差异影响，部署到真实极端情况时仍存在潜在风险。

#### 4.2 开放问题

1. **自进化伪专家生成**：如何利用预训练规划器的自进化方法迭代改进伪专家生成，突破规则基方法的覆盖上限？
2. **扩散式交通生成**：扩散式交通生成器能否在保持高速逼真度的同时显著增加场景多样性？
3. **sim-real gap 的系统性缓解**：如何系统性缓解仿真视觉伪影和分布差异带来的 sim-real gap？
4. **自博弈范式扩展**：自博弈范式能否进一步提升闭环鲁棒性并扩展长尾场景覆盖？
5. **场景采样策略优化**：调整仿真场景采样策略（如偏向高难度场景）对缩放趋势有何影响？

### 5. 知识库贡献定位

SimScale 的核心贡献在于**建立了一套可扩展的仿真数据生成与协训练框架**，并首次系统性地揭示了仿真数据规模与端到端规划器性能之间的**对数二次缩放律**（Eq. 7-8）。这一发现为自动驾驶领域的数据驱动扩展提供了可预测的理论指导，表明通过增加仿真数据规模，可以在不增加真实数据的情况下持续提升规划器的鲁棒性与泛化性。该方法已开源（[GitHub](https://github.com/OpenDriveLab/SimScale)），可作为后续研究的基线平台。



## 原文 PDF

![[paperPDFs/CVPR_2026/SimScale_Learning_to_Drive_via_Real_World_Simulation_at_Scale.pdf]]
