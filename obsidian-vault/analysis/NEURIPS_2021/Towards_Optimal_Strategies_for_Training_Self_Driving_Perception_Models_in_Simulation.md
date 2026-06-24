---
title: "Towards Optimal Strategies for Training Self-Driving Perception Models in Simulation"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/Towards_Optimal_Strategies_for_Training_Self_Driving_Perception_Models_in_Simulation.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/simulation-strategies/
aliases:
- LSA
- TOSTSDPMS
tags:
- NEURIPS_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "（1）数据生成阶段：通过设计空间先验（spatial prior）控制 NPC 位置采样，以减小合成数据与真实数据之间的标签边际分布 JSD 散度；（2）训练阶段：结合 Pearson χ² 域对抗损失（f-DAL）和强增强伪标签损失，在特征空间对齐分布的同时利用目标域高置信度预测。两者共同作用，从理论和实践上缩小 sim-to-real 差距。"
primary_logic: "从域自适应理论出发，模拟器的数据生成必须使标签边际分布充分接近（λ* 可忽略），才能让域对抗方法仅依靠最小化源域风险与特征空间域差异来实现有效迁移；同时，伪标签在对抗框架下可进一步暴露模型于真实数据，补偿模拟器在资产、天气等方面的不足。"
claims:
- "提出的空间先验采样策略将合成数据与 nuScenes 验证集的标签边际分布 JSD 从 1.40e-3 降至 5.7e-4，显著优于传统基于道路结构的采样。"
- "联合数据生成与训练策略（Ours）在 Lift-Splat BEV 车辆分割任务上将 IOU 从 9.76 (RS-No Adaptation) 提升至 17.84，超过所有基线。"
- "域对抗方法 f-DAL 优于 DANN，且结合伪标签后性能进一步提升；训练策略消融证实各组件的有效性。"
- "模型迁移 IOU 与标签边际分布间的 JSD 呈明显负相关，验证了理论下界（Theorem 2）的指导意义。"
---

# Towards Optimal Strategies for Training Self-Driving Perception Models in Simulation

> [!tip] 核心洞察
> 从域自适应理论出发，模拟器的数据生成必须使标签边际分布充分接近（λ* 可忽略），才能让域对抗方法仅依靠最小化源域风险与特征空间域差异来实现有效迁移；同时，伪标签在对抗框架下可进一步暴露模型于真实数据，补偿模拟器在资产、天气等方面的不足。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向模拟器中训练自动驾驶感知模型的最优策略 |
| 英文题名 | Towards Optimal Strategies for Training Self-Driving Perception Models in Simulation |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2111.07971); [Project](https://nv-tlabs.github.io/simulation-strategies); [Project](https://research.nvidia.com/labs/toronto-ai/simulation-strategies/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Lift-Splat-Adapt |
| Dataset | nuScenes validation (camera-based Lift-Splat), nuScenes validation (LiDAR-based PointPillars) |

> [!tip] 效果简介
> - nuScenes validation (camera-based Lift-Splat) 上，IOU 为 17.84 (Ours)，对比 9.76 (RS-No Adaptation)，变化 +8.08。
> - nuScenes validation (LiDAR-based PointPillars) 上，IOU 为 17.20 (Ours)，对比 15.09 (RS-No Adaptation)，变化 +2.11。

## 概述

**问题瓶颈**：在模拟器中训练自动驾驶感知模型的核心障碍并非模拟器本身的视觉真实感不足，而是合成数据与真实数据之间的**标签边际分布失配**。传统数据生成策略（如基于道路可行驶区域的 NPC 采样）会产生与目标域显著偏离的标签分布，导致即便采用域对抗学习方法，模型在真实场景中的迁移性能仍然受限。从域自适应理论出发，当标签边际分布的 Jensen-Shannon 散度（JSD）不可忽略时，联合风险存在不可逾越的下界（Theorem 2），仅靠特征空间对齐无法保证有效迁移。

**核心方法**：本文提出 **Lift-Splat-Adapt**，从数据生成与训练策略两个维度联合缩小 sim-to-real 差距：
- **数据生成端**：设计不依赖道路结构的**空间先验**（spatial prior）控制 NPC 位置采样，使合成数据的标签边际分布逼近真实数据，将 JSD 从 1.40e-3 降至 5.7e-4（Figure 2）。
- **训练端**：结合 **Pearson χ² 域对抗损失**（f-DAL）与**强增强伪标签损失**，在 BEV 特征空间对齐源域与目标域分布的同时，利用目标域高置信度预测提供额外监督信号。

**关键发现与定位**：
1. **理论指导实践**：迁移 IOU 与标签边际 JSD 呈显著负相关（Figure 7），验证了 Theorem 2 下界的工程意义——数据生成必须优先保证标签分布对齐。
2. **方法有效性**：在 nuScenes 验证集上，Lift-Splat-Adapt 将 BEV 车辆分割 IOU 从无适应基线的 9.76 提升至 17.84（Table 1）；在 LiDAR 点云模态（PointPillars）上同样获得 +2.11 IOU 的增益（Table 2）。
3. **域对抗与伪标签互补**：f-DAL 优于经典 DANN，且伪标签在对抗框架下进一步暴露模型于真实数据分布，可补偿模拟器在车辆资产数量、相机后处理等方面的真实感缺失（Figure 12, Figure 14）。
4. **方法谱系定位**：本文工作处于**域自适应理论驱动的仿真数据生成与训练**交叉点，区别于纯风格迁移（如 MUNIT）或标准对抗自适应（如 DANN），强调从标签边际对齐的根本问题出发进行系统设计。

**主要局限**：伪标签策略存在将行人区域误检为车辆的系统性偏差（Figure 15），对弱势交通参与者的感知安全性构成潜在风险；模型对罕见车型（如橙色巴士）及精确距离估计仍有不足。

## 背景与动机

自动驾驶系统依赖大规模、高质量标注数据来训练感知模型。然而，真实世界数据的采集与标注成本极高，且难以覆盖长尾场景。模拟器（如 CARLA）提供了一种可扩展的替代方案，能够以低成本生成无限量的标注数据。但模拟数据与真实数据之间存在显著的**领域差异（domain gap）**——合成图像在纹理、光照、资产多样性等方面与真实场景存在系统性偏差，导致在模拟器上训练的模型直接部署到真实环境时性能大幅下降。

现有应对这一差距的方法主要分为两类：一是通过**风格迁移**（如 MUNIT，Huang et al., ECCV 2018）将合成图像“翻译”为真实风格后再训练；二是采用**域自适应（domain adaptation）**方法，如 DANN（Ganin et al., JMLR 2016），在特征空间对齐源域与目标域分布。然而，这些方法在实践中仍面临根本性挑战。

从域自适应理论出发，目标域风险 $R_T^{\ell}(h)$ 受以下上界约束（Theorem 1）：

$$R_T^{\ell}(h) \leq R_S^{\ell}(h) + D_{h,\mathcal{H}}^{\phi}(P_s\|P_t) + \lambda^{*}$$

其中 $R_S^{\ell}(h)$ 为源域风险，$D_{h,\mathcal{H}}^{\phi}$ 为基于 $f$-散度的域差异度量，$\lambda^{*}$ 为理想联合假设风险。现有域对抗方法（如 DANN）聚焦于最小化特征空间的域差异 $D_{h,\mathcal{H}}^{\phi}$，却隐含假设 $\lambda^{*}$ 足够小。然而，**当源域与目标域的标签边际分布不匹配时，$\lambda^{*}$ 可能不可忽略**，此时即使完美对齐特征分布，也无法保证目标域性能。

Theorem 2 进一步揭示了标签边际分布差异的根本性影响：

$$R_T^{\ell}(h) + R_S^{\ell}(h) \geq \frac{1}{2} \left( \sqrt{D_{\mathrm{JS}}(P_s(y) \| P_t(y))} - \sqrt{D_{\mathrm{JS}}(P_s(z) \| P_t(z))} \right)^2$$

该下界表明：若标签边际分布间的 Jensen-Shannon 散度大于特征分布间的散度，则组合风险存在不可压缩的下限。这意味着**仅靠特征空间对齐无法弥合 sim-to-real 差距**——数据生成阶段的标签边际分布控制同样至关重要。

传统模拟器数据生成策略通常依赖道路结构或可行驶区域来采样非玩家角色（NPC）位置。这种采样方式会导致合成数据的标签边际分布与真实数据显著偏离（例如，车辆在 BEV 空间中的空间分布过于集中在道路中心），从而引入不可忽视的 $\lambda^{*}$。Figure 2 直观展示了这一现象：基于道路结构的采样策略使得 $P_s(y)$ 与 nuScenes 验证集的 $P_t(y)$ 之间的 JSD 高达 $1.40 \times 10^{-3}$。

综上，本文的核心动机在于：**从域自适应理论出发，系统性地解决模拟器训练中的标签边际分布不匹配问题**。具体而言，需要同时在两个层面进行干预——（1）**数据生成层面**：设计不依赖道路结构的采样策略，使合成数据的标签边际分布主动逼近真实分布；（2）**训练层面**：采用更强的域对抗损失（如 Pearson $\chi^2$ 散度）并结合目标域伪标签，在特征对齐的同时进一步利用目标域信息。两者协同，方能从理论与实践上缩小 sim-to-real 差距。

## 核心创新

本文的核心创新在于从域自适应理论出发，系统性地重新设计了模拟器训练的完整链条——不仅关注“如何训练”，更首次将“如何生成数据”纳入优化范畴，形成**数据生成与训练策略的联合最优**方案。

### 创新一：理论驱动的标签边际对齐采样

传统模拟器数据生成仅依赖道路可行驶区域的几何结构采样 NPC 位置（Road Structure，RS），忽略了合成数据与真实数据在标签边际分布 $P(y)$ 上的系统性偏移。本文从域自适应理论下界（Theorem 2）出发，揭示了关键瓶颈：

$$R_T^{\ell}(h) + R_S^{\ell}(h) \geq \frac{1}{2} \left( \sqrt{D_{\mathrm{JS}}(P_s(y) \| P_t(y))} - \sqrt{D_{\mathrm{JS}}(P_s(z) \| P_t(z))} \right)^2$$

该下界表明：**若标签边际散度 $D_{\mathrm{JS}}(P_s(y) \| P_t(y))$ 大于特征空间散度，则无论特征对齐多好，组合风险都存在不可逾越的下界**。这从根本上解释了为何单纯的域对抗训练（如 DANN）在 sim-to-real 场景下效果有限——当模拟器生成的标签分布与真实场景严重不匹配时，$\lambda^{*}$ 项无法忽略，Theorem 1 的上界也随之松弛。

针对这一理论洞察，本文提出**空间先验采样策略**（Spatial Prior），将 NPC 位置的概率密度设计为仅依赖于纵向距离的分段线性函数：

$$P_{\mathrm{spatial}}(x_1, x_2) \propto \left\{ {-\frac{1}{125}|x_2| + 0.6 \ |x_2| \leq 12.5} \atop {-\frac{1}{75}(|x_2| - 50) \ |x_2| > 12.5} \right.$$

该先验与横向位置 $x_1$ 无关，完全脱离道路结构约束，使生成的合成数据标签边际分布 $P_s(y)$ 更接近真实分布 $P_t(y)$。实验证实（Figure 2），空间先验将合成数据与 nuScenes 验证集的标签边际 JSD 从 RS 的 **1.40e-3 降至 5.7e-4**，降幅达 59%。更重要的是，Figure 7 显示迁移 IOU 与 JSD 呈显著负相关，直接验证了 Theorem 2 的指导意义——**标签边际对齐是域自适应成功的前提条件**。

### 创新二：f-DAL 与伪标签协同的域对抗训练

在数据生成侧保证标签边际对齐后，训练侧需要进一步缩小特征空间的域差异。本文提出将 **Pearson χ² 域对抗损失**（f-DAL）与**强增强伪标签损失**联合优化，形成双重域自适应机制。

**Pearson χ² 域判别器**：传统 DANN 使用标准对抗损失对齐特征分布，本文则采用基于 f-散度的 Pearson χ² 散度作为域差异度量：

$$d_{st} := \mathbb{E}_{x \sim p_s}\left[ \mathbb{E}_{h \cdot w}[(\hat{h}' \circ g)] \right] - \mathbb{E}_{x \sim p_t}\left[ \mathbb{E}_{h \cdot w}[\frac{1}{4}(\hat{h}' \circ g)_i^2 + \hat{h}' \circ g(x)_i] \right]$$

该损失通过 per-location 域分类器（两层 Conv + LeakyReLU，插入 BevEncoder 最终上采样模块之前）实现像素级域对齐。消融实验（Table 3）表明，**f-DAL 显著优于 DANN**，验证了 Pearson χ² 散度在密集预测任务上比标准对抗损失具有更强的分布对齐能力。

**强增强伪标签分支**：为进一步暴露模型于真实数据分布，本文引入基于置信度阈值 $\tau=0.9$ 的伪标签机制：

$$\ell_{\mathrm{pseudo}}(p, p_{\mathrm{aug}}) := \sum_{i=0}^{h \cdot w} \mathbb{1}[p_i \ge \tau] [\beta \log p_{\mathrm{aug}_i}] + \mathbb{1}[1 - p_i \le 1 - \tau] \log(1 - p_{\mathrm{aug}_i})$$

其关键设计在于：用**非增强目标域视图的高置信度预测**作为伪标签，监督**经 RandAugment + 相机丢弃强增强的目标域视图**。这种“弱监督强”的策略迫使模型在对抗训练的同时学习对真实数据增强的鲁棒性，且伪标签仅来自目标域自身，无需任何真实标注。

### 创新三：数据生成与训练策略的因果联动

本文的核心洞察在于**数据生成与训练策略并非独立优化**——只有当标签边际分布充分接近（$\lambda^{*}$ 可忽略）时，域对抗方法才能通过最小化源域风险与特征空间域差异来实现有效迁移。Table 3 的消融实验完整呈现了这一因果链：

- 在最佳数据生成策略（空间先验）下，RS-No Adaptation 的 IOU 仅为 10.35；
- 单独加入 f-DAL 提升至 16.03；
- 再加入伪标签损失（即完整 Ours）达到最优 **17.84**；
- 相比之下，若数据生成侧仍用 RS，即使采用相同的训练策略，性能上限也被显著压缩。

这种“生成-训练”联动机制还展现出对模拟器真实感缺失的强补偿能力：Figure 12 显示，当车辆资产数量从默认值降至极少时，Ours 的性能下降远小于 RS 基线；Figure 14 表明，即使关闭 CARLA 的相机后处理效果（降低图像真实感），域自适应训练仍能大幅补偿性能损失。这证明**本文方法学习到的是与渲染质量弱相关的语义特征，而非对纹理细节的过拟合**。

综上，本文的创新本质在于：**将域自适应理论从“训练时的特征对齐”前推至“生成时的分布匹配”，形成闭环优化**——空间先验从源头缩小 $D_{\mathrm{JS}}(P_s(y) \| P_t(y))$，f-DAL 在特征空间对齐 $P_s(z)$ 与 $P_t(z)$，伪标签提供目标域语义监督，三者协同使 Theorem 1 的上界真正收紧。

## 整体框架

Lift‑Splat‑Adapt 的整体 pipeline 由两条正交但协同的设计主线构成：**数据生成阶段**通过空间先验控制合成数据的标签边际分布，**训练阶段**则在域对抗框架下联合 Pearson χ² 散度对齐与强增强伪标签监督。两条主线共同服务于同一个理论目标——将 Theorem 2 下界中的标签边际散度 $D_{\mathrm{JS}}(P_s(y) \| P_t(y))$ 压到足够小，使 Theorem 1 中的 $\lambda^*$ 可忽略，从而让域不变表征学习真正生效。

### 模块拓扑与信息流

整个系统可抽象为三个逻辑层，其输入输出关系如下：

1. **数据生成模块（CARLA）**  
   - **输入**：CARLA 地图、天气/光照参数、车辆资产库、NPC 数量分布（匹配 nuScenes 统计量）、空间先验密度 $P_{\mathrm{spatial}}(x_1, x_2)$ 或道路结构采样规则。  
   - **处理**：根据所选采样策略在每帧中放置 NPC 车辆，同步抓取 6 路相机图像、LiDAR 点云、自车运动及 3D 包围盒标签。  
   - **输出**：合成源域样本 $(x_s, y_s) \sim P_s$，其中 $x_s$ 包含多视图 RGB 与 LiDAR，$y_s$ 为 BEV 车辆分割二值图。  
   - **关键设计**：NPC 位置仅依赖于纵向距离 $|x_2|$ 的空间先验（Equation 2），与道路几何解耦，使 $P_s(y)$ 的 JSD 相对 nuScenes 验证集从 $1.40 \times 10^{-3}$ 降至 $5.7 \times 10^{-4}$（Figure 2）。

2. **特征编码器 $g$（CamEncoder + BevEncoder）**  
   - **输入**：源域/目标域的多视角图像 $x$。  
   - **处理**：遵循 Lift‑Splat 架构，将每视图 2D 特征通过深度估计提升至 3D 视锥，再投影到统一的 BEV 特征空间 $Z$。  
   - **输出**：BEV 特征图 $z = g(x)$，作为分割头与域判别器的共享表示。  
   - **架构细节**：域判别器 $\hat{h}'$ 被插入在 BevEncoder 最终上采样模块之前（Figure 16），以保证判别器作用在语义足够丰富但空间分辨率可控的特征层上。

3. **分割头 $\hat{h}$ 与域判别器 $\hat{h}'$（对抗训练分支）**  
   - **输入**：BEV 特征 $z$。  
   - **处理**：  
     - $\hat{h}$ 将 $z$ 映射为车辆分割热图 $\hat{y}$；  
     - $\hat{h}'$（两层 Conv + LeakyReLU 的 per‑location 域分类器）对 $z$ 的每个空间位置输出域标签，计算 Pearson $\chi^2$ 散度损失 $d_{st}$（Equation 4）。  
   - **输出**：分割预测 $\hat{y}$ 与域差异标量 $d_{st}$。  
   - **梯度反转层（GRL）** 在 $g$ 与 $\hat{h}'$ 之间实现 minimax 优化：$g$ 被训练以最大化域分类误差，$\hat{h}'$ 则最小化该误差。

4. **伪标签分支（目标域自监督）**  
   - **输入**：目标域图像经弱增强（标准预处理）和强增强（RandAugment + 随机相机丢弃）得到的两个视图。  
   - **处理**：  
     - 弱增强视图通过 $g \circ \hat{h}$ 产生概率图 $p$；  
     - 对 $p$ 中置信度超过阈值 $\tau=0.9$ 的像素生成硬伪标签；  
     - 用这些伪标签监督强增强视图的预测 $p_{\mathrm{aug}}$，损失为 $\ell_{\mathrm{pseudo}}$（Equation 5）。  
   - **输出**：伪标签损失标量，与源域分割损失和域对抗损失联合反向传播。

### 训练目标与优化流程

整体训练目标为 minimax 形式（Equation 3）：

$$
\operatorname*{min}_{\hat{h}, g} \operatorname*{max}_{\hat{h}'} \; \underbrace{\mathbb{E}_{x,y \sim P_s}[\ell(\hat{h} \circ g, y)]}_{\text{源域分割损失}} + \underbrace{d_{st}}_{\text{Pearson }\chi^2\text{ 域差异}} + \underbrace{\ell_{\mathrm{pseudo}}}_{\text{伪标签损失}}
$$

其中 $\ell$ 为带正类权重 $\beta$ 的像素级二值交叉熵。三者通过共享的 $g$ 联合优化：源域损失提供任务监督，$d_{st}$ 强制特征空间域对齐，伪标签损失则利用目标域高置信度预测补偿模拟器在资产多样性、相机后处理等方面的真实感缺失（Figure 12、Figure 14 证实该补偿能力）。

### 关键设计决策与证据链

- **空间先验采样**是唯一不依赖真实标注即可大幅降低 $P_s(y)$ 与 $P_t(y)$ 间 JSD 的策略（Figure 2(c) vs (d)）。这直接响应了 Theorem 2 的理论要求：若标签边际散度大于特征散度，组合风险存在不可压缩的下界。  
- **Pearson $\chi^2$ 域损失**（$d_{st}$）相比标准 DANN 对抗损失在 BEV 分割任务上更有效（Table 3 消融证实 f‑DAL 优于 DANN）。  
- **伪标签分支**在域对齐基础上提供额外增益（Table 3），但其引入的行人误检偏差（Figure 15）提示伪标签质量控制在安全攸关场景中仍需谨慎处理。  
- **IOU 与 JSD 的负相关关系**（Figure 7）直接验证了理论下界的实践指导意义：标签边际对齐程度是 sim‑to‑real 迁移性能的强预测因子。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/011_Figure_7.jpg]]
*Figure 7: IOU vs. JSD Transfer performance is negatively correlated with the distance between Ps(y) and Pt(y) as expected from Theorem 2. Figure 8: Semi-Super. Learning Our method improves over baselines when p% of the labeled data is available at training*

> **注意**：关于伪标签阈值 $\tau$ 的自适应调整策略、方法在其他模拟器（AirSim、LGSVL）上的泛化性，以及扩展到全景分割等更密集预测任务的表现，目前缺乏实验证据，需进一步验证。

## 核心模块与公式推导

Lift-Splat-Adapt 的核心设计围绕一个中心命题展开：**若模拟器生成的标签边际分布与目标域显著偏离，则任何仅依赖特征空间对齐的域自适应方法都存在不可消除的下界**。这一命题由 Theorem 2 严格给出，并直接驱动了数据生成与训练两个阶段的模块设计。

### 理论下界：为什么标签边际对齐是必需的

设 $P_s(y)$ 和 $P_t(y)$ 分别为源域（模拟器）与目标域（真实场景）的标签边际分布，$P_s(z)$ 和 $P_t(z)$ 为特征空间 $Z$ 中的边际分布。Theorem 2 给出了源域与目标域联合风险的下界：

$$R_T^{\ell}(h) + R_S^{\ell}(h) \geq \frac{1}{2} \left( \sqrt{D_{\mathrm{JS}}(P_s(y) \| P_t(y))} - \sqrt{D_{\mathrm{JS}}(P_s(z) \| P_t(z))} \right)^2$$

其中 $D_{\mathrm{JS}}$ 为 Jensen-Shannon 散度。该不等式的关键含义是：**当标签边际散度大于特征散度时，无论特征空间对齐得多好，联合风险始终存在一个不可压缩的下界**。这意味着，若模拟器生成数据时不考虑标签边际对齐（例如 NPC 位置分布与真实交通流统计显著不同），即使后续使用域对抗方法学习不变表征，目标域性能仍受此下界约束。

这一理论洞察直接催生了两个层面的干预：**数据生成阶段的空间先验采样**（缩小 $D_{\mathrm{JS}}(P_s(y) \| P_t(y))$）和**训练阶段的 Pearson χ² 域对抗损失**（缩小 $D_{\mathrm{JS}}(P_s(z) \| P_t(z))$）。

### 数据生成模块：空间先验采样

标准模拟器数据生成通常基于道路可行驶区域的几何结构采样 NPC 位置——例如沿车道中心线或地图标注的可行驶区域放置车辆。这种策略导致合成数据的标签边际分布 $P_s(y)$ 与真实分布 $P_t(y)$ 之间存在显著差异（JSD = 1.40e-3，见 Figure 2）。

本文提出的**空间先验采样**完全脱离道路结构约束，仅依赖车辆相对于自车的纵向距离 $x_2$ 定义概率密度：

$$P_{\mathrm{spatial}}(x_1, x_2) \propto \begin{cases} -\frac{1}{125}|x_2| + 0.6, & |x_2| \leq 12.5 \\ -\frac{1}{75}(|x_2| - 50), & |x_2| > 12.5 \end{cases}$$

其中 $x_1$ 为横向位置（独立于概率密度），$x_2$ 为纵向距离（正值表示自车前方）。该密度的设计直觉来自对 nuScenes 数据集中车辆位置分布的观察：车辆密度随纵向距离增加而递减，且与横向位置弱相关。通过从该先验中采样 NPC 位置，合成数据的标签边际 JSD 降至 5.7e-4，与使用目标域标签估计的先验（3.2 节，JSD 约 4.5e-4）处于同一数量级，但**无需访问任何真实标签**（Figure 2c vs 2d）。

### 训练模块：Pearson χ² 域对抗损失与伪标签

在特征空间对齐层面，Lift-Splat-Adapt 采用 **f-DAL 框架下的 Pearson χ² 散度**替代标准 DANN 的二元交叉熵对抗损失。给定特征编码器 $g$、分割头 $\hat{h}$ 和域判别器 $\hat{h}'$，minimax 训练目标为：

$$\min_{\hat{h}, g} \max_{\hat{h}'} \ \mathbb{E}_{x,y \sim p_s}[\ell(\hat{h} \circ g, y)] + d_{st}$$

其中 $\ell$ 为带正类权重 $\beta$ 的像素级二值交叉熵：

$$\ell(p, q) := \frac{1}{h \cdot w} \sum_{i=0}^{h \cdot w} \beta p_i \log q_i + (1 - p_i) \log(1 - q_i)$$

域差异项 $d_{st}$ 采用 per-location 域分类器（两层 Conv + LeakyReLU）计算 Pearson χ² 散度：

$$d_{st} := \mathbb{E}_{x \sim p_s}\left[ \mathbb{E}_{h \cdot w}[(\hat{h}' \circ g)] \right] - \mathbb{E}_{x \sim p_t}\left[ \mathbb{E}_{h \cdot w}\left[\frac{1}{4}(\hat{h}' \circ g)_i^2 + \hat{h}' \circ g(x)_i\right] \right]$$

该设计的关键在于 **per-location 判别**：域分类器在 BEV 特征图的每个空间位置独立判断该位置来自源域还是目标域，而非对整个图像做全局域分类。这使得域对齐能关注局部空间位置的分布差异，对 BEV 分割任务尤为重要。

为进一步利用目标域信息，训练中引入**强增强伪标签损失**。对每个目标域样本，生成两个视图：弱增强视图（标准预处理）用于产生预测 $p$，强增强视图（RandAugment + 随机相机丢弃）用于计算损失。仅对置信度超过阈值 $\tau = 0.9$ 的像素生成伪标签：

$$\ell_{\mathrm{pseudo}}(p, p_{\mathrm{aug}}) := \sum_{i=0}^{h \cdot w} \mathbb{1}[p_i \ge \tau] [\beta \log p_{\mathrm{aug}_i}] + \mathbb{1}[1 - p_i \le 1 - \tau] \log(1 - p_{\mathrm{aug}_i})$$

该损失的作用是**将模型暴露于目标域的强增强变体**，利用高置信度预测作为监督信号，补偿模拟器在车辆资产多样性、相机后处理效果等方面的真实感缺失（Figure 12、Figure 14 验证了这一补偿效应）。

### 模块间因果链路

上述模块并非独立运作，而是通过理论下界形成因果链路：

1. **空间先验采样** 缩小 $D_{\mathrm{JS}}(P_s(y) \| P_t(y))$，降低 Theorem 2 下界，使域自适应方法有可优化的空间；
2. **Pearson χ² 域对抗损失** 在特征空间缩小 $D_{\mathrm{JS}}(P_s(z) \| P_t(z))$，直接优化 Theorem 1 中的域差异项；
3. **伪标签损失** 在对抗框架下提供目标域监督信号，使模型能在域对齐的同时从目标域高置信度区域学习。

Figure 7 的实验证据直接支持这一链路：迁移 IOU 与标签边际 JSD 呈明显负相关，与 Theorem 2 的理论预期一致。消融实验（Table 3）进一步证实，在固定最佳数据生成策略后，f-DAL 优于 DANN，且伪标签带来额外增益。

## 实验与分析

### 实验设置概览

本文构建了两条主要的 sim-to-real 迁移路径：基于相机的 Lift-Splat 模型和基于 LiDAR 的 PointPillars 模型，目标均为鸟瞰视角（BEV）下的车辆分割任务。源域数据由 CARLA 模拟器生成，目标域为 nuScenes 验证集。基线方法包括：

- **RS-No Adaptation**：仅使用道路结构采样和随机化参数训练，无任何域自适应。
- **RS-Style Transfer (MUNIT)**：基于 MUNIT（Huang et al., ECCV 2018）将 CARLA 图像风格迁移至 nuScenes 风格后再训练。
- **RS-DANN**：基于 DANN（Ganin et al., JMLR 2016）的标准域对抗训练。
- **RS-Ensemble** 及 **RS-Ensemble + Test-time Aug**：利用真实标签选择最优预测的集成方法，代表当前任务上的性能上界。

本文提出的方法称为 **Lift-Splat-Adapt**，其核心由三部分构成：空间先验数据采样、Pearson χ² 域对抗损失（f-DAL）、以及强增强伪标签损失。

### 主要结果

**Table 1** 展示了基于 Lift-Splat 的 BEV 车辆分割结果。在完全不使用 nuScenes 真实标注的情况下，本文方法（Ours）取得了 **17.84 IOU**，相比 RS-No Adaptation 的 9.76 IOU 提升了 **+8.08**，且显著优于 RS-Style Transfer（11.47）和 RS-DANN（14.25）。值得注意的是，本文方法甚至超过了使用真实标签的 RS-Ensemble（16.50），仅略低于 RS-Ensemble + Test-time Aug（18.71）这一性能上界。

**Table 2** 展示了基于 PointPillars 的 LiDAR 分割结果。本文方法取得 **17.20 IOU**，相比 RS-No Adaptation 的 15.09 IOU 提升 +2.11，并优于 RS-DANN 的 16.55。LiDAR 模态上的提升幅度小于相机模态，这与 LiDAR 点云本身对域差异较不敏感的特性一致，但联合数据生成与训练策略的优势仍然显著。

### 消融实验

**Table 3** 在固定最佳数据生成策略的前提下，对训练策略进行了组件消融。结果表明：

1. **f-DAL 优于 DANN**：使用 Pearson χ² 散度的域对抗损失比标准 DANN 对抗损失带来更稳定的域对齐效果。
2. **伪标签带来额外增益**：在 f-DAL 基础上加入强增强伪标签损失（τ=0.9）后，性能进一步提升，验证了目标域高置信度预测的利用价值。
3. **联合策略最优**：空间先验采样 + f-DAL + 伪标签的组合达到最高 IOU，各组件贡献相互补充。

**Figure 7** 揭示了迁移 IOU 与标签边际分布间 JSD 的负相关关系。随着合成数据与 nuScenes 验证集的标签边际 JSD 降低，模型迁移性能单调提升，这与 Theorem 2 的理论下界预期一致——当标签边际散度大于特征散度时，组合风险存在不可压缩的下界。**Figure 2** 量化了这一关键机制：空间先验采样将 JSD 从传统道路结构采样的 1.40e-3 降至 **5.7e-4**，为后续域对抗训练创造了有利条件。

### 模拟器真实感缺失的补偿能力

本文进一步考察了域自适应方法对模拟器固有不足的补偿效果（见 **Figure 12** 和 **Figure 14**）：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/015_Figure_12.jpg]]
*Figure 12: Vehicle Assets (Left) We vary the number of vehicle assets used when sampling CARLA data. Interestingly, Lift-Splat-Adapt (ours) is able to compensate for performance when very few assets are used. (Middle) We compare performance when the number of NPCs per episode is sampled from Unif(0, 40), fixed at 1/10/20/30/40 NPCs per episode, or sampled from the distribution in Figure 4. Finally, we compare performance on datasets in which car colors are independently sampled from $\mathrm { U n i f } ( \bar { 0 }$ , x ) vs. default car colors

- **车辆资产数量**（Figure 12 左）：当 CARLA 中可用车辆资产从默认数量减少至极少时，RS-No Adaptation 性能急剧下降，而 Lift-Splat-Adapt 能够大幅补偿这一损失，表明域自适应降低了对资产多样性的依赖。
- **相机后处理**（Figure 14）：关闭 CARLA 的相机后处理效果（如 bloom、镜头光晕等）会显著降低图像真实感。RS-No Adaptation 在此设置下性能大幅退化，而 Lift-Splat-Adapt 几乎完全补偿了真实感损失，说明域对抗和伪标签机制能够学习到对渲染细节不变的表征。
- **交通模型**（Figure 13）：是否使用交通模型控制 NPC 行为对最终性能无显著影响，表明空间先验采样已能提供足够的标签边际对齐，NPC 的具体运动模式并非关键因素。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/016_Figure_13.jpg]]
*Figure 13: Traffic Model Performance is unaffected by whether or not a traffic model is used when generating synthetic data*

### 泛化性与鲁棒性

**Figure 9** 展示了不同采样策略对城镇泛化性的影响。当 NPC 采样依赖于特定城镇的道路几何结构时，模型在不同城镇间的迁移性能波动较大；而空间先验采样由于独立于道路结构，显著提升了跨城镇的鲁棒性。这一结果进一步验证了“数据生成不应过度拟合特定场景布局”的设计原则。

**Figure 8** 的半监督学习实验表明，即使有少量目标域标注数据可用，本文方法仍能持续提升性能并优于各基线，说明空间先验采样和域自适应策略与半监督范式兼容。

### 失败模式与局限性

**Figure 15** 展示了 Lift-Splat-Adapt 最优模型的典型失败案例，揭示了三个系统性不足：

1. **罕见车型漏检**：模型无法检测车库中的橙色巴士。这是因为模拟器资产库中缺乏该车型的充分覆盖，域自适应无法凭空补全未见类别的视觉概念。
2. **行人误检为车辆**：模型将行人区域（尤其是腿部可见的行人）错误预测为车辆。这源于伪标签策略的偏差——模型错误关联了行人身体部位与车辆部件的视觉特征，且高置信度伪标签会强化这一错误关联。该偏差对行人等弱势交通参与者的感知安全性构成潜在风险，需在后续工作中通过多类别联合建模或伪标签质量过滤加以缓解。
3. **距离估计偏差**：模型将后方车辆预测得过分靠近自车，表明 BEV 特征空间中的深度推理仍存在系统性误差，可能源于单帧图像到 BEV 的几何投影不确定性。

### 理论验证总结

综合 **Figure 7** 的 IOU-JSD 负相关趋势与 **Table 3** 的消融结果，实验证据一致支持本文的核心理论主张：模拟器的数据生成必须使标签边际分布充分接近目标域（λ* 可忽略），才能让域对抗方法仅依靠最小化源域风险与特征空间域差异来实现有效迁移。空间先验采样将 JSD 降至 5.7e-4 量级，为这一条件提供了实践基础；而 f-DAL 与伪标签的联合优化则进一步在特征空间对齐分布并暴露模型于真实数据，补偿模拟器在资产、渲染等方面的不足。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/009_Table_3.jpg]]
*Table 3: Ablation on the Training Strategy. In this scenario, we fix the datageneration strategy to be the best*

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/004_Figure_4.jpg]]
*Figure 4: Matching nuScenes Statistics From left to right, we show the distribution of number of vehicles per scene in nuScenes, the distribution of field of view of the nuScenes cameras, the yaw relative to the ego coordinate frame of the cameras (6 peaks for the 6 different camera directions), and the height of the LiDAR (roughly the same across all scenes). These statistics are matched when sampling data from CARLA*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/010_Figure_9.jpg]]
*Figure 9: Better Sampling Improves Town Robustness We compare transfer performance of Lift Splat models when NPCs are sampled according to geometry of the town roads (left) vs the hard-coded prior (right). Performance greatly improves when using a sampling strategy that doesn’t condition on road structure*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/018_Figure_15.jpg]]
*Figure 15: Limitations Predictions of the best Lift Splat Adapt model vs. ground-truth when the model makes an error. (Left) The model does not detect the orange bus in the garage. (Middle) The model predicts a vehicle where there are pedestrians. (Right) The model predicts a car behind it is much closer than it actually is*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/007_Table_1.jpg]]
*Table 1: Lift-Splat Sim → Real. We compare the performance of our method vs RS. To account for the reality gap, we also show results of RS with different adaptation techniques*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2111_07971/figures/008_Table.jpg]]

## 方法谱系与知识库定位

### 1. 与基线工作的关系

**Lift-Splat-Adapt** 的定位是在模拟器训练自动驾驶感知模型的“数据生成—训练算法”联合优化框架。其核心贡献可从两个维度与既有基线形成对比。

#### 1.1 数据生成策略的突破

传统模拟器数据生成方法（本文统称为 **RS** 基线）依赖道路可行驶区域的几何结构采样 NPC 位置，并随机化颜色、天气等视觉参数。这种方法在直觉上试图覆盖多样性，但忽视了域自适应理论中的关键约束——**标签边际分布的对齐**。本文通过 Theorem 2 严格指出：若合成数据与真实数据的标签边际散度（JSD）大于特征空间散度，则组合风险存在不可消除的下界，即无论表征学习多强，迁移性能都存在理论上限。

本文提出的**空间先验采样**（Spatial Prior）直接针对这一瓶颈：设计仅依赖于纵向距离的概率密度函数
$$P_{\mathrm{spatial}}(x_1, x_2) \propto \left\{ {-\frac{1}{125}|x_2| + 0.6 \ |x_2| \leq 12.5} \atop {-\frac{1}{75}(|x_2| - 50) \ |x_2| > 12.5} \right.$$
使 NPC 位置采样独立于道路结构。实验证据表明，该策略将合成数据与 nuScenes 验证集的标签边际 JSD 从 **1.40e-3 降至 5.7e-4**（Figure 2），且这一降低与迁移 IOU 呈明显负相关（Figure 7），直接验证了 Theorem 2 的指导意义。相比之下，RS 的基于道路结构采样（包括按地图可行驶区域采样）无法有效控制标签边际散度，这是其性能瓶颈的结构性原因。

#### 1.2 域自适应算法的改进

在训练策略层面，本文与以下基线形成递进关系：

- **RS-No Adaptation**（无域自适应）：仅用道路结构采样和随机化参数训练，在 Lift-Splat BEV 车辆分割任务上 IOU 仅 **9.76**，作为性能下界。
- **RS-Style Transfer (MUNIT)**（Huang et al., ECCV 2018）：通过 MUNIT 将 CARLA 图像风格迁移至 nuScenes 风格后再训练。该方法仅在像素空间进行外观对齐，未涉及特征空间或标签空间的分布匹配，因此对域差异的补偿有限。
- **RS-DANN**（Ganin et al., JMLR 2016）：基于标准对抗损失的域对抗方法，对齐源域与目标域的特征分布。本文的 f-DAL 损失（基于 Pearson χ² 散度）在 DANN 基础上进行了两个关键改进：(1) 使用 per-location 域分类器适配密集预测任务；(2) 采用 Pearson χ² 散度替代标准二值交叉熵，理论上更适用于分布对齐。消融实验（Table 3）证实 f-DAL 优于 DANN。
- **RS-Ensemble / RS-Ensemble + Test-time Aug**：利用真实标签选择最优预测的集成方法，代表性能上界。本文方法虽未达到该上界，但在完全无真实标签的条件下显著缩小了差距。

#### 1.3 与半监督学习的关联

Lift-Splat-Adapt 的伪标签分支（基于置信度阈值 τ=0.9 筛选高置信度预测，并用强增强视图进行监督）在形式上与半监督学习中的一致性正则化方法相似。但本文的伪标签机制是在域对抗框架内运作的——伪标签不仅提供目标域监督信号，还与域判别器共同优化，使模型在对抗训练中暴露于更多真实数据的变化模式。Figure 8 表明，当部分真实标签可用时（半监督场景），本文方法仍持续优于基线，说明伪标签与域对抗之间存在协同效应。

### 2. 适用边界

#### 2.1 有效的前提条件

Lift-Splat-Adapt 的有效性建立在以下前提之上：

1. **标签边际可被先验近似**：空间先验采样假设真实场景中车辆的空间分布具有特定的纵向距离模式。这一假设在 nuScenes 数据集上得到了验证（Figure 2），但在交通流模式显著不同的场景（如高速公路、乡村道路）中可能需要重新校准先验参数。
2. **域差异主要体现在外观和布局层面**：本文的域对抗方法主要对齐特征空间分布，对几何形变、传感器噪声等物理层面的差异依赖伪标签和数据增强来补偿。消融实验（Figure 14）表明，当关闭 CARLA 的相机后处理效果时，本文方法仍能大幅补偿真实感损失，说明其对视觉外观差异具有较强鲁棒性。
3. **任务为单类别密集预测**：本文验证任务为 BEV 车辆分割（二值分割），扩展到多类别分割或全景分割时，标签边际的定义和先验设计需要重新考虑。

#### 2.2 不适用或需谨慎的场景

- **罕见目标类型**：Figure 15 显示模型无法检测模拟器资产库中未覆盖的橙色巴士，说明方法对资产多样性的补偿存在上限。当目标域包含合成数据中完全未见的目标类别时，域对抗和伪标签均无法提供有效监督。
- **行人等弱势交通参与者**：伪标签策略可能将行人区域（尤其是腿部与自行车共存时）误检为车辆。这种系统性偏差源于模型错误关联了行人身体部位与车辆部件的视觉特征，对安全性敏感的应用构成潜在风险。
- **精确距离估计**：模型对目标距离的估计仍存在系统性偏差（Figure 15），说明 BEV 特征空间的对齐尚不能完全解决几何推理的域差异。

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **资产覆盖依赖性**：方法能补偿资产数量少带来的性能下降（Figure 12），但无法完全消除未见资产类型导致的漏检。
2. **伪标签偏差**：基于置信度的伪标签筛选可能放大模型对特定类别的偏见，尤其在类别不平衡的场景中。
3. **距离估计偏差**：域对抗和伪标签主要作用于语义层面，对几何推理精度的提升有限。

#### 3.2 开放问题

1. **跨模拟器泛化**：本文的空间先验和训练策略均在 CARLA 上验证，其在 AirSim、LGSVL 等其他模拟器及更复杂传感器配置下的有效性尚未得到验证。
2. **自适应阈值与损失权重**：伪标签阈值 τ 和域损失权重 λ 目前为固定值。是否能根据目标域的数据特性（如场景复杂度、类别分布）自适应调整这些超参数，以在不同条件下保持稳定性能？
3. **扩展到密集多类别任务**：当任务从二值车辆分割扩展到全景分割等多类别密集预测时，标签边际的对齐策略和域判别器的设计需要何种调整？
4. **物理感知域自适应**：对于极端天气、动态光照等更复杂的物理域差异，是否需要引入更显式的物理模型（如大气散射模型、光照模型）来辅助域自适应？
5. **伪标签质量提升**：如何通过不确定性估计、多视图一致性等机制进一步提升伪标签质量，并减轻错误伪标签对弱势交通参与者的偏见？

## 原文 PDF

![[paperPDFs/NEURIPS_2021/Towards_Optimal_Strategies_for_Training_Self_Driving_Perception_Models_in_Simulation.pdf]]
