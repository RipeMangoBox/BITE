---
title: "Diffusion Forcing Planner: History-Annealed Planning with Time-Dependent Guidance for Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diffusion_Forcing_Planner_History_Annealed_Planning_with_Time_Dependent_Guidance_for_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- DFPDDFFM
- DFPHAPTDGAD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 推理时历史退火无分类器引导(CFG)的权重 w（历史引导强度）和退火速度 β（历史噪声化速度），可在稳定性与响应性之间实现可控权衡。
primary_logic: 将视频扩散生成中的扩散强制(Diffusion Forcing)范式迁移到运动规划，通过在训练中对历史、当前、未来块分配独立噪声水平并联合去噪，迫使模型学习片段间的因果依赖；推理时构造历史退火分支与无历史分支，利用无分类器引导可控地融合二者输出，从而解耦时间一致性与实时响应性。
claims:
- 分块独立噪声水平训练（Diffusion Forcing）使模型在历史信息部分缺失或完全噪声化的条件下学习稳定的因果条件生成。
- 历史退火CFG推理通过可调参数w和β实现稳定性与灵活性的连续控制，消融实验中完整DFP(A7)在Val14上达到NR 90.33 / R 79.97，显著优于未使用历史或使用静态历史的变体。
- DFP在nuPlan Val14、Test14及Test14-hard三个基准上均达到领先的闭环性能，尤其在高速场景下舒适度指标(+30 points vs. Diffusion Planner)证明了历史引导对稳定性的提升。
- 历史引导的最优超参数组合为 w = 0.2, β = 2.0，过强或过弱的历史引导均会损害综合得分。
---

# Diffusion Forcing Planner: History-Annealed Planning with Time-Dependent Guidance for Autonomous Driving

> [!tip] 核心洞察
> 将视频扩散生成中的扩散强制(Diffusion Forcing)范式迁移到运动规划，通过在训练中对历史、当前、未来块分配独立噪声水平并联合去噪，迫使模型学习片段间的因果依赖；推理时构造历史退火分支与无历史分支，利用无分类器引导可控地融合二者输出，从而解耦时间一致性与实时响应性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散强制规划器：历史退火与时变引导的自动驾驶规划 |
| 英文题名 | Diffusion Forcing Planner: History-Annealed Planning with Time-Dependent Guidance for Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Diffusion_Forcing_Planner_History-Annealed_Planning_with_Time-Dependent_Guidance_for_Autonomous_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Diffusion Forcing Planner (DFP) / DFP-FM (结合Flow Matching采样器) |
| Dataset | nuPlan Val14, nuPlan Test14-hard |

> [!tip] 效果简介
> - nuPlan Val14 (Non-Reactive) 上，Overall Score (%) 90.33 (DFP) / 92.68 (DFP-FM) vs 87.87 (Diffusion Planner*) / 89.87 (Diffusion Planner original report) (+2.46 / +2.81)。
> - nuPlan Val14 (Reactive) 上，Overall Score (%) 79.97 (DFP) / 81.30 (DFP-FM) vs 77.48 (Diffusion Planner*) / 82.80 (Diffusion Planner original report) (+2.49 / -1.50)。
> - nuPlan Test14-hard (Non-Reactive) 上，Overall Score (%) 76.91 (DFP) / 79.43 (DFP-FM) vs 74.26 (Diffusion Planner*) / 75.99 (Diffusion Planner original report) (+2.65 / +3.44)。

## 概述

**核心问题与瓶颈。** 扩散策略在闭环自动驾驶规划中存在两个根本性缺陷：一是**时间不一致性**，连续帧之间的轨迹预测缺乏平滑过渡；二是**因果混淆**（causal confusion），将历史轨迹作为静态条件输入会导致模型机械地复制历史模式，无法根据环境变化做出灵活决策。

**核心洞察。** 本文提出**扩散强制规划器**（Diffusion Forcing Planner, DFP），将视频生成中的扩散强制范式迁移到运动规划。训练时，将完整轨迹划分为历史、当前、未来三个片段，为每个片段独立分配噪声水平并联合去噪，迫使模型学习片段间的因果依赖关系；推理时，构建历史退火分支与无历史分支，利用无分类器引导（CFG）可控地融合二者输出，从而解耦时间一致性与实时响应性。

**方法定位。** DFP 在扩散解码器层面引入两项关键创新：① **分块级独立噪声调度**（噪声即掩码机制），替代传统扩散规划器中全轨迹统一噪声的做法；② **历史退火 CFG 推理**，通过可调参数——历史引导强度 $w$ 和退火速度 $\beta$——实现稳定性与灵活性的连续控制。DFP 的编码器沿用 **Diffusion Planner**（Zheng et al., ICLR 2025）的结构，同时提供了结合 Flow Matching 采样器的 DFP-FM 变体。

**主要结果。** 在 nuPlan 闭环评测的三个基准上，DFP 均达到领先水平：
- **Val14** 非反应式 90.33 / 反应式 79.97（相较 Diffusion Planner 提升 +2.46 / +2.49）；
- **Test14-hard** 非反应式 76.91（提升 +2.65）；
- 高速场景下舒适度指标提升 **30+ 点**（96.97 vs. ~66），验证了历史引导对轨迹稳定性的显著增益。

消融实验确认，完整方案（分块扩散强制训练 + 历史退火 CFG）在非反应式与反应式场景下均达到最优综合性能，最优超参数组合为 $w=0.2$、$\beta=2.0$。

## 背景与动机

自动驾驶中的运动规划本质上是一个序列决策问题：车辆需要在动态环境中生成安全、平滑且符合交通规则的未来轨迹。近年来，扩散模型因其强大的多模态分布建模能力，在运动规划中展现出巨大潜力，能够同时捕获场景中多种可能的未来演变。然而，现有扩散规划方法面临两个根本性挑战。

**时间不一致性。** 扩散策略在闭环驾驶中逐帧独立采样未来轨迹，缺乏跨时间步的显式一致性约束。这导致连续帧之间预测的轨迹可能出现抖动或突变，尤其在高速场景下，轨迹的不稳定性会严重损害乘坐舒适性和安全性。如图 2 所示，基线方法 Diffusion Planner（Zheng et al., ICLR 2025）在连续四帧中生成的轨迹存在明显漂移，而本文方法保持了高度的时间一致性。

**因果混淆。** 现有方法通常将历史轨迹作为静态条件直接输入编码器，模型倾向于机械地复制历史模式，而非根据当前环境变化做出灵活决策。这种“因果混淆”在交互密集或需要突然变道的场景中尤为致命——模型可能因过度依赖历史惯性而无法及时响应动态障碍物。**PlanTF**（Cheng et al., ICRA 2024）虽引入了历史 dropout 机制，但其随机丢弃策略缺乏可控性，难以在稳定性与响应性之间实现精细调节。

本文的核心动机在于：**能否设计一种扩散规划范式，既保留历史信息带来的时间一致性优势，又避免因果混淆导致的反应迟钝？** 受视频生成领域扩散强制（Diffusion Forcing）范式的启发，本文提出将轨迹视为时间序列片段，通过分块独立噪声训练迫使模型学习片段间的因果依赖关系，并在推理时引入可调的历史退火无分类器引导机制，实现稳定性与灵活性的连续可控权衡。

## 核心创新

本文的核心贡献在于将视频生成领域的**扩散强制（Diffusion Forcing）**范式迁移至自动驾驶运动规划，并提出**历史退火无分类器引导（History-Annealed CFG）**推理机制，从训练和推理两个层面系统性地解决了扩散策略在闭环驾驶中的两大瓶颈：**时间不一致性**与**因果混淆（causal confusion）**。这一方案通过三个关键设计槽位（changed slots）实现了对基线方法**Diffusion Planner**（Zheng et al., ICLR 2025）的本质性改进。

### 槽位一：分块独立噪声调度——噪声即掩码

**基线做法**：Diffusion Planner 对整条未来轨迹施加统一的扩散时间步，历史轨迹被完全忽略，模型仅从当前状态和场景上下文直接生成未来。

**DFP 改进**：将完整轨迹显式划分为历史块、当前块和未来块，对每个块独立采样噪声水平 $t_b \sim U(0,1)$，而当前块固定在 $t_{cur}=0$ 作为硬边界（hard boundary）。这一设计实现了**噪声即掩码（Noising-as-Masking）**机制——噪声水平越高，对应块的信息被遮蔽越强，迫使模型在历史信息部分缺失甚至完全噪声化的条件下，学习从当前状态到未来的因果条件生成关系。训练损失分别对历史块和未来块计算 $\mathbf{x}_0$ 预测的均方误差（Eq. 4），通过权重 $\lambda_{hist}$ 和 $\lambda_{futr}$ 平衡历史重建与未来预测的学习。

这一设计直接回应了因果混淆问题：传统方法将干净历史作为静态条件输入，导致模型机械复制历史模式；DFP 通过训练中随机遮蔽历史片段，迫使模型学习“在给定不同程度历史信息的情况下如何做出合理规划”，从而在推理时能够根据实际需求灵活调节对历史的依赖程度。

### 槽位二：历史信息利用方式——从静态条件到可控引导

**基线做法**：Diffusion Planner 完全忽略自车历史轨迹，仅依赖当前状态和场景上下文进行规划，虽然避免了因果混淆，但丧失了历史信息带来的时间一致性。

**DFP 改进**：训练阶段联合预测历史与未来，使模型内化片段间的时序依赖关系；推理阶段构建**双分支 CFG 架构**：
- **未引导分支（unguided branch）**：将历史块替换为纯噪声，模拟“无历史先验”的条件生成；
- **引导分支（guided branch）**：按退火调度逐步恢复历史块，从纯噪声退火至干净信号。

两分支的输出通过线性融合 $\hat{X}_0 = \hat{X}_{0,unguided} + w(\hat{X}_{0,guided} - \hat{X}_{0,unguided})$ 得到最终预测（Eq. 8），其中引导强度 $w \in [0,1]$ 控制历史信息的影响程度。这一设计将历史从“静态输入条件”转变为“可调引导信号”，使规划器在时间一致性与环境响应性之间获得了连续可控的权衡空间。

### 槽位三：推理采样策略——双分支 CFG 与退火调度

**基线做法**：标准扩散采样，单次前向传播生成未来轨迹，无历史引导机制。

**DFP 改进**：推理时运行双分支并行的扩散去噪过程，核心在于引导分支的**历史退火调度** $X_{guidance} = \alpha(t)X_{history} + \sigma(t)\varepsilon$，其中 $t = (t_s)^\beta$（Eq. 6）。退火速度 $\beta \geq 1$ 控制历史信息的恢复节奏：$\beta$ 越大，早期扩散步骤的历史噪声越强，模型在采样初期更依赖当前观测和环境上下文进行全局规划，仅在最后几步才注入精细的历史轨迹信息以平滑输出。

消融实验（Table 3）系统验证了三个槽位的贡献：基础 Diffusion Planner（A1）性能最低；引入分块动作建模（A3）带来明显提升；进一步加入分块级独立噪声（A4，即 Diffusion Forcing）使训练更稳定；在无分块情况下引入历史引导（A5）增益有限；分块建模配合静态干净历史（A6）虽有所提升，但历史过强导致策略反应迟钝；最终方案 A7（分块 Diffusion Forcing + 历史退火 CFG）在非反应式（NR 90.33）和反应式（R 79.97）场景下均达到最佳综合性能。超参数网格扫描（Figure 3）进一步揭示最优组合为 $w=0.2, \beta=2.0$，过弱或过强的历史引导均会损害综合得分，验证了可控历史引导的必要性。

### 方法谱系与知识库定位

DFP 处于**扩散生成式规划**与**序列条件生成**的交叉点。其核心训练范式——分块独立噪声的扩散强制——源自视频预测领域的 Diffusion Forcing 框架，本文首次将其迁移至运动规划任务。与现有扩散规划器的关系：

- **Diffusion Planner**（Zheng et al., ICLR 2025）：DFP 的直接基线，继承其场景编码器架构，但通过分块噪声调度和历史退火 CFG 解决了其时间不一致和因果混淆问题。
- **CoPlanner**（Zhong et al., arXiv 2025）：同为基于扩散的交互式规划器，但侧重于 contingency-aware 的多模态预测，未引入历史引导机制。
- **PlanTF**（Cheng et al., ICRA 2024）：基于 Transformer 的模仿学习规划器，通过历史 dropout 缓解因果混淆，但缺乏扩散模型的分布建模能力和可控采样机制。
- **PDM-Open**（nuPlan 官方规则基规划器）：代表非学习方法的性能上界，DFP 在学习基方法中达到领先水平。

DFP 的核心知识贡献在于：**通过训练阶段的随机噪声遮蔽与推理阶段的可控退火引导，将“历史信息的利用”从被动条件输入升级为主动调节变量**，为扩散策略在闭环序贯决策任务中的应用提供了新的范式。

## 整体框架

Diffusion Forcing Planner (DFP) 将视频生成领域的**扩散强制（Diffusion Forcing）**范式迁移至自动驾驶运动规划，核心目标是解决扩散策略在闭环驾驶中的两个根本性瓶颈：**时间不一致性**与**因果混淆**。其整体框架围绕“分块独立噪声训练—双分支历史退火推理”这一主轴构建，形成从场景编码到轨迹生成的端到端流水线。

### 框架总览

整个 DFP 流水线由五个核心模块串联而成，数据流自上而下为：场景上下文编码 → 轨迹分块与分词 → 块级时态嵌入注入 → DiT 解码器联合去噪 → 历史退火 CFG 推理融合。Figure 1 给出了框架的宏观示意。

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Diffusion Forcing Planner framework*

**输入层**接收三类信息：
- 场景上下文 $C$（高精地图、周围智能体状态等）
- 导航路线 $R$
- 自车历史轨迹 $x_0^{-H}, \dots, x_0^{-1}$ 与当前状态 $x_0^0$

**输出层**为未来 $F$ 步的规划轨迹 $\hat{x}_0^1, \dots, \hat{x}_0^F$，每步包含坐标与航向的四元组。

### 模块关系与数据流

**场景编码器**沿用 Diffusion Planner（Zheng et al., ICLR 2025）的编码器架构，将场景上下文 $C$ 和导航路线 $R$ 编码为统一的条件向量，作为后续 DiT 解码器中交叉注意力的记忆张量。该模块不参与扩散噪声过程，仅提供静态场景先验。

**分块轨迹分词与位置编码**将完整轨迹按固定长度 $L$ 划分为 $N$ 个块（chunk），每块作为一个 token。具体而言，历史、当前、未来三部分被分割为 $N_H$ 个历史块、1 个当前块和 $N_F$ 个未来块。每个块通过线性投影映射到 token 特征空间，并叠加可学习位置嵌入，形成初始 token 序列。这一分块设计是扩散强制训练的基础——它使得不同时间段的轨迹片段可以作为独立单元被差异化噪声化。

**块级时态嵌入**为每个 token 生成独立的扩散时间步嵌入。该嵌入通过正弦傅里叶特征加 MLP 实现，并与导航信息 $R$ 广播求和，形成逐 token 的调节向量 $y$。$y$ 随后注入 DiT 解码器的自适应层归一化（adaLN）中，控制每个块的去噪强度。这一机制是“噪声即掩码（Noising-as-Masking）”的技术实现——噪声水平 $t_b$ 越高，对应块的信息被掩蔽越强，迫使模型从其他块和场景上下文中推理缺失片段。

**DiT 解码器块**由堆叠的 DiT（Diffusion Transformer）层组成，每层包含两个注意力子层：
- **多头自注意力（MHSA）**：沿 token 轴操作，跨越历史、当前、未来块，捕捉片段间的长程因果依赖。这是模型学习“历史→未来”条件生成结构的关键。
- **多头交叉注意力（MHCA）**：以每个 token 为查询，从场景上下文记忆 $C$ 中提取空间与交互先验，注入到每个轨迹片段。

两个子层均通过 adaLN 接受调节向量 $y$ 的调制，公式为：
$$\tilde{x} = \tilde{x} + \text{MHSA}(\text{adaLN}(\tilde{x}, y))$$
$$\tilde{x} = \tilde{x} + \text{MHCA}(\text{adaLN}(\tilde{x}, y), C)$$

**历史退火 CFG 推理模块**是 DFP 推理阶段的核心创新。与训练时单分支联合去噪不同，推理时构造两个并行分支：
- **未引导分支**：将历史块替换为纯噪声 $\varepsilon$，仅依赖当前块和场景上下文进行未来预测。
- **引导分支**：将历史块按退火调度 $X_{\text{guidance}} = \alpha(t)X_{\text{history}} + \sigma(t)\varepsilon$ 逐步注入干净历史信号，其中 $t = (t_s)^\beta$，$\beta$ 控制退火速度。

两个分支的输出通过无分类器引导（CFG）线性融合：
$$\hat{X}_0 = \hat{X}_{0,\text{unguided}} + w(\hat{X}_{0,\text{guided}} - \hat{X}_{0,\text{unguided}})$$

其中引导强度 $w \in [0,1]$ 控制历史信息的影响程度。最终将融合后的未来块拼接，并在块间重叠区域施加线性羽化平滑，消除边界不连续性。

### 训练-推理协同设计

DFP 的训练与推理并非独立设计，而是形成闭环协同：

| 阶段 | 历史块处理 | 当前块处理 | 核心机制 |
|------|-----------|-----------|---------|
| **训练** | 独立采样噪声水平 $t_b \sim U(0,1)$ | 固定 $t_{\text{cur}}=0$（硬边界） | 分块联合去噪，学习因果条件生成 |
| **推理** | 双分支：纯噪声 vs. 退火历史 | 固定 $t_{\text{cur}}=0$ | CFG 融合，可控权衡稳定性与响应性 |

训练中当前块噪声固定为 0 构成“硬边界”，将历史与未来锚定在当前时刻，防止因果信息跨越边界泄露。训练时历史块噪声采样自 Beta 分布，使更多样本集中在 $t \approx 0$（干净历史）和 $t \approx 1$（纯噪声）两端，增强模型对历史信息不同程度缺失的鲁棒性。这一训练策略直接支撑了推理时的历史退火机制——模型已学会在历史从纯噪声到完全干净的整个谱系上进行条件生成。

### 关键设计决策与因果机制

DFP 解决因果混淆的核心机制在于**训练-推理的不对称设计**：训练时强制模型在历史信息部分缺失的条件下预测未来，打破了“历史干净→复制历史模式”的捷径；推理时通过可调参数 $w$ 和 $\beta$ 在稳定性（依赖历史保持时间一致性）与响应性（忽略历史以适应环境变化）之间实现连续控制。消融实验（Table 3）证实，完整方案（A7）在 Val14 上达到 NR 90.33 / R 79.97，显著优于仅使用静态历史（A6）或完全无历史（A1）的变体。

> **注意**：DFP-FM 变体将扩散采样器替换为 Flow Matching 采样器，在保持框架不变的前提下进一步提升采样效率与性能，其流水线结构与 DFP 完全一致。

## 核心模块与公式推导

### 问题形式化

DFP 将运动规划建模为一个条件生成问题：从源分布 $p_{0}(x_{0})$（纯噪声）出发，经过扩散去噪过程，逐步变换到目标分布 $q(x_{1}|C, H, w)$，其中 $C$ 为场景上下文，$H$ 为历史轨迹，$w$ 为历史引导因子。这一形式化将历史信息从“静态条件”重新定位为“可调控的先验”，为后续的分块训练与退火推理奠定基础。

### 分块轨迹定义与噪声即掩码机制

完整的自车轨迹被划分为历史、当前和未来三个时域：

$$x_{0} = [x_{0}^{-H}, ..., x_{0}^{0}, ..., x_{0}^{F}] \in \mathbb{R}^{S \times 4}, \quad S = H + 1 + F$$

其中每个状态为 4 元组（坐标与航向）。为进一步引入结构先验，轨迹按固定长度 $L$ 被分割为 $N$ 个块（chunk），第 $b$ 个块的干净子序列定义为：

$$\boldsymbol{x}_{0}^{(b)} = [x_{0,i}^{(b)}]_{i \in \mathcal{T}_{b}} \in \mathbb{R}^{1 \times 4L}, \quad b = 1, 2, ..., N$$

核心创新在于**分块独立噪声水平采样**。对每个块 $b$，独立采样噪声时间步 $t_b \sim U(0, 1)$，并通过扩散 SDE 的边缘分布进行扰动：

$$\boldsymbol{x}_{t_b}^{(b)} = \alpha(t_b) \boldsymbol{x}_{0}^{(b)} + \sigma(t_b) \boldsymbol{\varepsilon}^{(b)}, \quad \boldsymbol{\varepsilon} \sim \mathcal{N}(0, 1)$$

这一设计实现了**噪声即掩码（Noising-as-Masking）**：当 $t_b \to 1$ 时，该块被完全噪声化（等价于“掩码”）；当 $t_b \to 0$ 时，该块保持干净信号。特别地，当前块（current chunk）的噪声水平固定在 $t_{cur}=0$，形成硬边界（hard boundary），为规划提供时间锚点，防止未来轨迹在去噪过程中发生漂移。

### 扩散强制训练损失

训练时，模型接收全部 $N$ 个被不同程度噪声化的块，联合预测所有块的干净版本 $\hat{\boldsymbol{x}}^{(b)}$。损失函数分别对历史块和未来块计算 $\ell_2$ 重建误差，当前块（$t=0$）不参与损失计算：

$$\mathcal{L}_{\mathrm{denoise}} = \frac{\lambda_{\mathrm{hist}}}{N_H} \sum_{b=1}^{N_H} \mathbb{E}_{t_b, x_{0}^{(b)}} \left[\lVert \hat{\boldsymbol{x}}^{(b)} - \boldsymbol{x}_{0}^{(b)} \rVert_{2}^{2}\right] + \frac{\lambda_{\mathrm{futr}}}{N_F} \sum_{b=N_H+2}^{N} \mathbb{E}_{t_b, x_{0}^{(b)}} \left[\lVert \hat{\boldsymbol{x}}^{(b)} - \boldsymbol{x}_{0}^{(b)} \rVert_{2}^{2}\right]$$

其中 $N_H$ 和 $N_F$ 分别为历史块和未来块的数量，$\lambda_{\mathrm{hist}}$ 和 $\lambda_{\mathrm{futr}}$ 为平衡权重。由于每个块接收独立的噪声水平，模型被迫学习在历史信息部分缺失或完全噪声化的条件下进行条件生成，从而建立块间的**因果依赖**，而非机械地复制历史模式——这正是解决因果混淆（causal confusion）的关键机制。

### 历史退火无分类器引导推理

推理阶段，DFP 构建两个并行分支：

- **未引导分支（unguided branch）**：将历史块全部替换为纯噪声，迫使模型仅依赖场景上下文 $C$ 生成未来轨迹。
- **引导分支（guided branch）**：历史块按退火调度逐步注入干净信号：

$$X_{\mathrm{guidance}} = \alpha(t) X_{\mathrm{history}} + \sigma(t) \varepsilon, \quad t = (t_s)^{\beta}$$

其中 $t_s$ 为当前扩散步骤 $s$ 的归一化时间，$\beta \geq 1$ 为退火速度参数。当 $\beta$ 较大时，早期步骤中历史接近于纯噪声，仅在最后几步恢复为干净历史，从而在生成早期保留更大的探索空间。

两个分支的输出通过无分类器引导（CFG）进行线性融合：

$$\hat{X}_{0} = \hat{X}_{0,\mathrm{unguided}} + w \big( \hat{X}_{0,\mathrm{guided}} - \hat{X}_{0,\mathrm{unguided}} \big)$$

其中 $w \in [0, 1]$ 为历史引导强度。$w \to 0$ 时模型更灵活但可能不稳定，$w \to 1$ 时模型更稳定但可能反应迟钝。最终，融合后的未来块与历史块在重叠区域采用线性羽化（linear feathering）平滑拼接，确保轨迹连续性。

### 解码器架构

轨迹的 $N$ 个块首先通过线性投影和可学习位置嵌入转换为 token 特征。每个 token 接收独立的扩散时间步嵌入（正弦傅里叶特征 + MLP），并与导航信息 $R$ 广播求和形成逐 token 调节向量 $y$。随后，堆叠的 DiT 块通过自适应层归一化（adaLN）将 $y$ 注入注意力计算：

$$\tilde{x} = \tilde{x} + \mathrm{MHSA}(\mathrm{adaLN}(\tilde{x}, y))$$

$$\tilde{x} = \tilde{x} + \mathrm{MHCA}(\mathrm{adaLN}(\tilde{x}, y), C)$$

其中 MHSA 沿 token 轴（覆盖历史、当前、未来块）捕捉长程依赖，MHCA 将场景上下文 $C$ 注入每个 token。场景编码器沿用 Diffusion Planner 的编码器结构，将场景上下文和导航路线编码为条件向量。

## 实验与分析

### 闭环评测主结果

Table 1 报告了 DFP 及 DFP-FM 在 nuPlan 三个基准上的闭环评测结果。所有方法均直接使用原始模型输出，不添加任何后处理模块，以保证公平比较。其中 Diffusion Planner* 为作者多次复现的最优结果，可能略低于原论文报告值。

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/002_Table_1.jpg]]
*Table 1: Main results on the nuPlan benchmarks. Overall score (%) in non-reactive (NR) and reactive (R) closed-loop evaluations on Val14, Test14, and Test14-hard. Raw model outputs are evaluated without additional post-processing for fair comparison. *: The best result from our multiple reimplementation attempts, slightly differing from the original report. DFP-FM combines DFP with the Flow Matching sampler*

在 Val14 非反应式（NR）设定下，DFP 达到 90.33% 的综合得分，较 Diffusion Planner*（87.87%）提升 +2.46 个百分点；结合 Flow Matching 采样器的 DFP-FM 进一步提升至 92.68%。在反应式（R）设定下，DFP 取得 79.97%，较 Diffusion Planner*（77.48%）提升 +2.49 个百分点。在更具挑战性的 Test14-hard 非反应式设定下，DFP 达到 76.91%，DFP-FM 达到 79.43%，分别超出 Diffusion Planner* 的 74.26% 达 +2.65 和 +5.17 个百分点。这些结果表明，历史退火引导机制在多种闭环场景下均带来一致且显著的性能增益。

**Table 1** 展示了完整的方法间对比，包括 PDM-Open、UrbanDriver、GameFormer、PlanTF、PLUTO、CoPlanner 等基线。DFP 在所有学习型基线中达到领先水平，尤其在非反应式场景下优势突出。

### 分场景细粒度分析

Table 2 在 Val14 非反应式设定下对 DFP、Diffusion Planner（DP）和 PlanTF 进行了分场景指标对比。各场景指标均为布尔型，报告满足条件的案例比例（越高越好）。

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/003_Table_2.jpg]]
*Table 2: Case study on scenario-specific metrics. Evaluation is conducted on the nuPlan Val14 benchmark in the non-reactive setting. The number following each scenario type indicates the count of samples belonging to that scene. “DP” denotes the Diffusion Planner baseline; Score denotes the overall score for the scenario; Collision/TTC/Drivable/Comfort/Progress denote the respective per-scenario metrics. All per-scenario metrics are Boolean indicators, reported as the fraction of cases satisfying the condition (higher is better)*

DFP 在高速场景（High magnitude speed）下取得 94.95 的综合得分，显著优于 DP（84.50）和 PlanTF（89.39）。在舒适度（Comfort）指标上，DFP 在高速场景达到 96.97%，而 Diffusion Planner 仅约 66%，提升超过 30 个百分点。这一巨大差距直接验证了历史引导对轨迹稳定性的关键作用——在高速行驶中，历史信息的平滑约束能够有效抑制帧间轨迹抖动，从而大幅提升乘坐舒适度。

在中等速度场景（Moderate）和静止场景（Stationary）中，DFP 同样保持领先或持平。在交叉口穿越（Traversal）等需要灵活响应的场景中，DFP 得益于可控的历史引导机制，在稳定性和响应性之间取得了更好的平衡。

### 消融实验：扩散解码器设计的影响

Table 3 系统消融了扩散解码器中各设计组件对 Val14 NR 和 R 性能的影响，共设置 7 个变体：

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/004_Table_3.jpg]]
*Table 3: Effect of designs in the diffusion decoder. Ablations on Val14 under Non-Reactive (NR) and Reactive (R) evaluation*

- **A1（基础 Diffusion Planner）**：无分块、无历史、标准扩散训练，NR 和 R 性能均为最低基线。
- **A3（引入分块动作建模）**：在 A1 基础上将轨迹划分为块进行建模，性能出现明显提升，表明分块结构本身有助于捕捉轨迹的局部时序依赖。
- **A4（分块级独立噪声 / Diffusion Forcing）**：在分块建模基础上为每块独立采样噪声水平，训练过程更稳定，NR 和 R 性能进一步提升。这验证了“噪声即掩码”机制使模型在历史信息部分缺失的条件下学会了稳定的因果条件生成。
- **A5（无分块 + 历史引导）**：在未分块的情况下引入历史引导，增益有限，说明历史引导需要与分块结构协同才能发挥作用。
- **A6（分块 + 静态干净历史）**：分块建模配合完整干净的历史作为条件，虽然性能提升，但历史信号过强导致策略反应迟钝，在反应式场景中表现不佳。
- **A7（完整 DFP：分块 Diffusion Forcing + 历史退火 CFG）**：在 NR 和 R 场景下均达到最佳综合性能，验证了可控历史引导机制的有效性——训练阶段的 Diffusion Forcing 使模型学会从部分噪声化的历史中推理，推理阶段的历史退火 CFG 则通过可调参数在稳定性与灵活性之间实现连续控制。

### 超参数敏感性分析

Figure 3 展示了历史引导权重 $w$ 和退火速度 $\beta$ 的网格扫描结果。实验表明，最优超参数组合为 $w = 0.2$、$\beta = 2.0$。当 $w \to 0$（几乎无历史引导）时，模型退化为类似 Diffusion Planner 的行为，轨迹稳定性下降；当 $w \to 1$（完全依赖历史引导）时，模型过度复制历史模式，对动态环境变化的响应能力减弱，综合得分同样下降。$\beta$ 控制历史退火的速度：$\beta = 2.0$ 使早期扩散步骤接近于纯噪声，仅最后几步恢复为干净历史，从而在采样早期保留足够的探索空间，后期注入历史约束以确保一致性。

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/006_Figure_3.jpg]]
*Figure 3: Effect of history guidance weights*

### 定性分析

Figure 2 展示了 DFP 与 Diffusion Planner 在连续四帧中的轨迹预测对比。Diffusion Planner 由于完全忽略自车历史，在相邻帧之间出现明显的轨迹跳变和不一致；DFP 通过历史退火引导，保持了更平滑、时间上更一致的轨迹，尤其在弯道和交互场景中优势显著。

![[assets/figures/papers/paper_list_l2463_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Diffusion_Forcin/figures/005_Figure_2.jpg]]
*Figure 2: DP vs. DFP qualitative comparison. The figure visualizes trajectory predictions over four consecutive frames in two scenarios. Yellow trajectories denote expert (log-replay) trajectories and blue trajectories denote model predictions. Compared to DP, DFP maintains smoother and more temporally consistent trajectories across frames*

### 失败模式与局限

尽管 DFP 在整体指标上表现领先，仍存在以下局限：

1. **超参数依赖**：历史分块长度 $L$、总块数 $N$、引导权重 $w$ 和退火速度 $\beta$ 均需手动设定，对特定场景类型可能不够鲁棒。当前缺乏根据环境上下文自适应调节的机制。
2. **实时性未验证**：双分支 CFG 推理需要两次前向传播，论文未分析计算时延，在真实自动驾驶硬件上的端到端延迟是否满足实时要求尚需验证。
3. **泛化性有限**：仅在 nuPlan 数据集上验证，尚未在真实车辆或其他驾驶数据集上进行测试。
4. **反应式场景仍有差距**：在反应式闭环设定下，DFP 与部分基线（如原版 Diffusion Planner 报告值 82.80%）相比仍有提升空间，表明在高度交互场景中历史引导与实时响应之间的平衡仍需进一步优化。

## 方法谱系与知识库定位

### 1. 与扩散策略规划器的关系

DFP 的核心贡献在于将视频生成中的 **扩散强制（Diffusion Forcing）** 范式迁移至自动驾驶运动规划领域。与现有扩散规划器相比，其关键差异体现在三个维度：

**（1）历史信息利用方式的根本转变。** 主流扩散规划器——特别是作为 DFP 直接基线的 **Diffusion Planner**（Zheng et al., ICLR 2025）——在推理时完全忽略自车历史轨迹，仅以当前状态和场景上下文作为条件生成未来轨迹。这种设计虽然避免了因果混淆（causal confusion），但也导致规划器缺乏时间连续性，在连续帧之间产生轨迹跳变（Figure 2 定性对比提供了直观证据）。DFP 则通过分块独立噪声训练和推理时历史退火 CFG，在稳定性与响应性之间建立了可控的权衡机制。

**（2）噪声调度策略的粒度提升。** 传统扩散规划器对全轨迹或未来轨迹使用统一的扩散时间步（单一噪声水平），而 DFP 将轨迹划分为历史、当前、未来三个区段，每段内的每个块独立采样噪声水平 $t_b \sim U(0,1)$，当前块固定在 $t=0$ 作为硬边界。这种“噪声即掩码”（Noising-as-Masking）机制迫使模型在历史信息部分缺失或完全噪声化的条件下学习稳定的因果条件生成，从而在训练阶段即内化了时间一致性约束。

**（3）推理策略的范式创新。** DFP 将无分类器引导（CFG）从传统的条件增强工具重新定位为历史信息强度的连续调节器。推理时构建双分支——引导分支使用按退火调度 $\alpha(t) X_{\text{history}} + \sigma(t) \varepsilon$ 逐步恢复的历史块，未引导分支使用纯噪声替代历史块——并通过线性融合 $\hat{X}_{0} = \hat{X}_{0,\text{unguided}} + w(\hat{X}_{0,\text{guided}} - \hat{X}_{0,\text{unguided}})$ 实现可控的历史引导。这一设计使得单个模型可覆盖从“完全忽略历史”（$w=0$）到“完全复制历史模式”（$w=1$）的连续行为谱。

### 2. 与其他学习型规划器的关系

**基于模仿学习的规划器。** **PlanTF**（Cheng et al., ICRA 2024）通过历史 dropout 技术缓解因果混淆，但本质上仍将历史作为确定性条件输入，缺乏推理时的动态调节能力。**UrbanDriver**（Scheel et al., CoRL 2022）和 **PLUTO**（Cheng et al., arXiv 2024）分别采用策略梯度和概率模仿学习，但均未显式建模历史信息的不确定性。DFP 的分块扩散强制训练可视为一种更系统的历史条件建模方法——通过随机化历史噪声水平，模型被迫学习从任意质量的历史信号中提取有效信息。

**基于博弈论的规划器。** **GameFormer**（Huang et al., ICCV 2023）通过 Transformer 架构建模多智能体交互，**CoPlanner**（Zhong et al., arXiv 2025）进一步引入 contingency-aware 的扩散规划。这些方法与 DFP 在技术路线上正交：前者关注交互建模的精度，后者关注时间一致性的机制设计。DFP 的历史退火 CFG 框架可与上述交互建模方法结合，形成更完整的规划系统。

**规则型规划器。** **PDM-Open** 作为 nuPlan 官方基准，代表了基于规则的工程化方案。DFP 在 Val14 非反应式场景下以 90.33% 的综合得分超越 PDM-Open，证明了学习型方法在闭环驾驶中的潜力。

### 3. 适用边界与局限

**已知适用场景。** 实验证据表明 DFP 在以下条件下表现突出：(a) 高速驾驶场景——Table 2 中高速场景舒适度指标达 96.97，较 Diffusion Planner 提升 30+ 点，说明历史引导对高速场景的轨迹平滑性至关重要；(b) 需要时间一致性的连续规划——Figure 2 定性对比显示 DFP 在连续四帧中的轨迹稳定性显著优于无历史的 DP；(c) 非反应式闭环评估——DFP 在 Val14、Test14 和 Test14-hard 的非反应式设置下均取得领先。

**已知局限。** 论文明确指出的限制包括：(a) 分块长度 $L$ 和总块数 $N$ 需手动设定，可能对特定驾驶场景不够鲁棒；(b) 历史引导权重 $w$ 和退火速度 $\beta$ 依赖人工调参（网格扫描确定 $w=0.2, \beta=2.0$ 为最优），缺乏根据环境上下文自适应调节的机制；(c) 仅在 nuPlan 数据集上验证，尚未在真实车辆或其他驾驶数据集上进行泛化测试；(d) 论文未分析双分支 CFG 推理的计算时延，可能对实时性产生影响。

**需要手动验证的边界。** 以下推断缺乏直接实验证据：(a) 在极端交互场景（如密集车流中的强制变道）下，历史引导是否会过度约束规划器的探索空间，导致碰撞率上升——Table 3 消融中 A6（干净静态历史）在反应式场景下性能下降提供了间接线索，但需进一步验证；(b) 分块扩散强制训练是否对轨迹长度 $S$ 敏感，当规划时域扩展到数百步时是否会导致训练不稳定或因果泄露。

### 4. 开放问题

**自适应历史引导。** 当前 $w$ 和 $\beta$ 为全局固定超参数，能否设计场景自适应的调节机制——例如基于注意力权重或元学习——使模型在简单场景下降低历史依赖以提升响应性，在复杂场景下增强历史引导以保证稳定性？这一问题直接关系到 DFP 在实际部署中的鲁棒性。

**长时域扩展性。** 分块扩散强制训练能否扩展到更长的规划时域（如数百步），而不会因块间因果依赖的累积导致训练不稳定？这涉及扩散强制范式在序列决策任务中的根本能力边界。

**实时推理可行性。** 双分支 CFG 推理的计算开销是否满足自动驾驶的实时要求（通常 < 100ms）？是否可以通过知识蒸馏、单步采样（如 Flow Matching 采样器的 DFP-FM 变体）或分支共享等策略加速？

**跨任务泛化。** 历史退火机制是否同样适用于其他序列决策任务（如机器人操控、无人机导航），以解决普遍存在的因果关系混淆问题？这决定了 DFP 的方法论贡献能否超越自动驾驶领域，形成更广泛的影响。

## 原文 PDF

![[paperPDFs/CVPR_2026/Diffusion_Forcing_Planner_History_Annealed_Planning_with_Time_Dependent_Guidance_for_Autonomous_Driving.pdf]]
