---
title: "DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DriveMoE_Mixture_of_Experts_for_Vision_Language_Action_Model_in_End_to_End_Autonomous_Driving.pdf
project_link: "https://thinklab-sjtu.github.io/DriveMoE/"
code_link: null
aliases:
- DriveMoE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入混合专家（MoE）架构进行视觉和决策的双重专项化：在视觉侧通过场景特化的Vision MoE动态选择上下文相关的相机视图，减少冗余；在动作侧通过技能特化的Action MoE激活不同的专家模块，实现行为解耦，避免模式平均。
primary_logic: 借鉴人类驾驶认知——驾驶员会根据场景有选择地关注关键视野，并在不同驾驶技能间灵活切换——通过可学习的路由器在视觉和动作两个层面实现上下文感知的专家选择，提高效率和泛化能力。
claims:
- DriveMoE (Traj-Level) 在 Bench2Drive 闭环评测上达到 DS 74.22、SR 48.64%，显著超越基线 Drive-π0（DS 55.85、SR 30.00%）
- 动态视图选择结合监督让 DS 从 55.85 提升至 74.22，成功率提升 62%
- 轨迹级 Action MoE 明显优于令牌级（DS 73.88 vs 65.62）
- 移除 Vision MoE 或 Action MoE 均导致性能显著下降，验证两个模块不可或缺
---

# DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving

> [!tip] 核心洞察
> 借鉴人类驾驶认知——驾驶员会根据场景有选择地关注关键视野，并在不同驾驶技能间灵活切换——通过可学习的路由器在视觉和动作两个层面实现上下文感知的专家选择，提高效率和泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | DriveMoE：面向端到端自动驾驶的视觉-语言-动作混合专家模型 |
| 英文题名 | DriveMoE: Mixture-of-Experts for Vision-Language-Action Model in End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.16278) · [Project](https://thinklab-sjtu.github.io/DriveMoE/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DriveMoE |
| Dataset | Bench2Drive Closed-Loop, Bench2Drive Multi-Ability, nuScenes Open-Loop |

> [!tip] 效果简介
> - Bench2Drive Closed-Loop 上，Driving Score (DS) ↑ 74.22 (DriveMoE Traj-Level) vs 55.85 (Drive-π0) (+18.37)；Success Rate (SR) ↑ 48.64% (DriveMoE Traj-Level) vs 30.00% (Drive-π0) (+18.64%)。
> - Bench2Drive Multi-Ability 上，Mean Ability (%) ↑ 47.91 (DriveMoE Traj-Level) vs 33.37 (Drive-π0) (+14.54)。
> - nuScenes Open-Loop 上，L2 Average (m) ↓ / Collision Avg (%) ↓ 0.74 / 0.17 (DriveMoE) vs 0.78 / 0.24 (Drive-π0) (-0.04 / -0.07)。

## 概述

端到端自动驾驶将原始传感器数据直接映射为车辆控制信号，近年来视觉-语言-动作（VLA）模型在这一范式下展现出巨大潜力。然而，现有 VLA 方案面临两大瓶颈：**多视图视觉处理**导致令牌冗余和巨大计算开销，模型收敛困难；**统一策略网络**偏向常见驾驶场景，难以有效处理罕见但关键的驾驶行为（如紧急刹车、激进转弯），产生模式平均效应。

针对上述问题，本文提出 **DriveMoE**，一种基于混合专家（Mixture-of-Experts, MoE）架构的端到端自动驾驶框架。其核心洞察借鉴了人类驾驶认知——驾驶员会根据场景有选择地关注关键视野，并在不同驾驶技能间灵活切换。DriveMoE 通过两个互补的 MoE 模块实现这一机制：

- **场景特化视觉混合专家（Scene-Specialized Vision MoE）**：通过可学习的视觉路由器，根据实时驾驶上下文动态选择一张上下文相关的额外相机视图，减少多视图冗余，提升感知效率。
- **技能特化动作混合专家（Skill-Specialized Action MoE）**：在条件流匹配规划器中集成 MoE 层，包含共享专家和多个非共享技能专家，由动作路由器根据驾驶意图激活不同的专家模块，实现行为解耦，避免模式平均。

在 Bench2Drive 闭环评测基准上，DriveMoE（轨迹级）达到 **Driving Score 74.22、成功率 48.64%**，相比基线 Drive-π0（DS 55.85、SR 30.00%）分别提升 18.37 分和 18.64 个百分点。消融实验表明，动态视图选择结合监督信号使成功率提升 62%，轨迹级 Action MoE 明显优于令牌级，且两个 MoE 模块均不可或缺。在多能力评测中，DriveMoE 尤其在 Merging、Emergency Brake 等罕见行为上相较基线有大幅提升，验证了技能专项化对长尾场景的泛化优势。

## 背景与动机

端到端自动驾驶旨在直接从传感器输入映射到车辆控制指令，省去传统模块化管线中的中间表征。近年来，视觉-语言-动作（Vision-Language-Action, VLA）模型在具身智能领域展现出强大的泛化能力，促使研究者将其引入自动驾驶。然而，将 VLA 范式直接迁移到端到端驾驶面临两个核心瓶颈。

**瓶颈一：多视图视觉冗余与计算膨胀。** 自动驾驶车辆通常配备多台环视相机，现有 VLA 方法（如 Figure 1a 所示的朴素视觉令牌编码）将所有环视图输入视觉塔，产生大量冗余令牌，导致计算开销激增且收敛困难。基于查询的令牌抽取方法（如 Q-Former，Figure 1b）虽能减少令牌数，但会丢失空间结构信息，且需要额外的预训练。一个关键观察是：人类驾驶员在不同场景下会选择性关注关键视野，而非同时处理所有环视信息——这一认知机制在现有方法中未被有效利用。

**瓶颈二：统一策略网络导致“模式平均”效应。** 现有端到端驾驶模型通常采用单一策略头处理所有驾驶场景（Figure 1d），这使其偏向高频出现的常规驾驶行为（如车道保持），而在罕见但安全关键的驾驶行为（如紧急刹车、激进转弯、匝道汇入）上表现不佳。这种模式平均效应严重制约了模型在长尾场景下的安全性。

针对上述瓶颈，本文提出 **DriveMoE**，一种基于混合专家（Mixture-of-Experts, MoE）架构的端到端自动驾驶框架。核心思路借鉴人类驾驶的认知机制——驾驶员会根据场景选择性关注关键视野，并在不同驾驶技能间灵活切换——在视觉和动作两个层面引入可学习的路由器，实现上下文感知的专家选择：

- **场景特化视觉混合专家（Scene-Specialized Vision MoE）**：通过 Vision Router 根据实时驾驶上下文动态选择与当前场景最相关的相机视图（Figure 1c），减少视觉令牌冗余，提升感知效率。
- **技能特化动作混合专家（Skill-Specialized Action MoE）**：在基于流匹配（flow-matching）的轨迹规划器中集成多个专家模块，由 Action Router 根据驾驶意图激活不同的专家（Figure 1e），实现行为解耦，避免模式平均。

DriveMoE 以 **Drive-π0** 作为基础模型——这是本文从具身智能领域迁移适配的 VLA 基线。在 Bench2Drive 闭环评测上，DriveMoE 的 Driving Score 从基线的 55.85 提升至 74.22，成功率从 30.00% 提升至 48.64%，尤其在 Merging、Emergency Brake 等罕见行为上相比基线有大幅提升（Table 1），验证了双重 MoE 架构在提升端到端驾驶效率与长尾泛化能力方面的有效性。

## 核心创新

DriveMoE 的核心创新在于将**混合专家（Mixture-of-Experts, MoE）架构**系统性地引入端到端自动驾驶的视觉-语言-动作（VLA）模型，在**视觉感知**和**动作规划**两个关键环节实现双重专项化，从而突破现有方法的瓶颈。

### 创新动机：两大瓶颈

现有 VLA 端到端自动驾驶模型面临两个根本性难题：

1. **多视图视觉冗余**：传统方法将所有环视图像送入视觉编码器，导致令牌冗余和巨大的计算开销，模型收敛困难。
2. **行为模式平均**：统一的策略网络倾向于拟合常见驾驶场景，难以有效处理罕见但关键的驾驶行为（如紧急刹车、激进转弯），产生“模式平均”效应，在长尾场景中表现不佳。

DriveMoE 借鉴人类驾驶认知——驾驶员会根据场景有选择地关注关键视野，并在不同驾驶技能间灵活切换——通过可学习的路由器在视觉和动作两个层面实现上下文感知的专家选择。

### Changed Slot 1：从固定双视图到场景特化动态视图选择

**基线方案（Drive-π0）**：仅使用两张连续前视图作为视觉输入，虽然避免了环视冗余，但丢失了侧向和后方的关键感知信息。

**DriveMoE 方案**：引入**场景特化视觉混合专家（Scene-Specialized Vision MoE）**，通过一个可学习的 Vision Router 动态选择一张上下文相关的额外相机视图（Top-1），与前视图共同构成视觉输入。Vision Router 以前视图嵌入和目标航点 ${\pmb g}_t$ 为输入，输出所有相机视图的选择概率分布：

$${\pmb p}_t = \mathrm{S}(\mathrm{o}(R_{\mathrm{vision}}(e_t^{\mathrm{front}}, {\pmb g}_t)))$$

训练时通过交叉熵损失进行监督，使用二值相机视图选择标注：

$$\mathcal{L}_{\mathrm{Vision-Router}} = -\lambda_0 \sum_{v=1}^{N} {\pmb y}_t^v \log({\pmb p}_t^v)$$

这一设计在保持令牌效率的同时，显著增强了模型对关键场景信息的感知能力。消融实验表明，动态视图选择结合监督信号将 Driving Score 从 55.85 提升至 74.22，成功率提升 62%（Table 3, Exp 1 vs Exp 9）。

### Changed Slot 2：从单一密集解码器到技能特化动作专家

**基线方案（Drive-π0）**：动作解码器采用单一密集前馈网络（FFN）的 flow-matching 轨迹解码器，所有驾驶行为共享同一组参数。

**DriveMoE 方案**：将解码器中的 FFN 替换为**技能特化动作混合专家（Skill-Specialized Action MoE）**层，包含 1 个共享专家和 6 个非共享技能专家，由 Action Router 动态激活 Top-3 专家。Action Router 将隐藏表征映射为专家概率分布：

$$r_k^{(\ell-1)} = \mathrm{Softmax}(R_{\mathrm{action}}({\bf h}^{(\ell-1)})), \quad k \in \{1, 2, \ldots, K\}$$

MoE 层的输出为非共享专家输出的加权和与共享专家输出之和：

$${\pmb h}^{(\ell)} = \sum_{k=1}^{K} {\pmb r}_k^{(\ell-1)} {\pmb y}_k^{(\ell-1)} + \sum_{m=1}^{M} {\pmb y}_m^{(\ell-1)}$$

在**轨迹级（Trajectory-Level）**变体中，Action Router 对整个轨迹序列取平均后再进行专家选择，使专家激活与完整驾驶行为语义对齐。训练时通过驾驶技能标签进行监督：

$$\mathcal{L}_{\mathrm{Action-Router}} = -y_k \log(r_k)$$

最终动作损失为流匹配轨迹损失与路由器损失的加权组合：

$$\mathcal{L}_{\mathrm{Action}} = \lambda_1 \mathcal{L}_{\mathrm{FM}} + \lambda_2 \mathcal{L}_{\mathrm{Action-Router}}$$

轨迹级 Action MoE 显著优于令牌级方案（DS 73.88 vs 65.62，Table 5），验证了行为级解耦的有效性。在多能力评测中，DriveMoE 尤其在 Merging、Emergency Brake 等罕见行为上比基线有大幅提升（Table 1）。

### Changed Slot 3：从单阶段训练到两阶段专家引导

**基线方案（Drive-π0）**：标准单阶段端到端训练。

**DriveMoE 方案**：采用**两阶段训练策略**：
- **第一阶段**：强制使用真实标签专家（ground-truth expert selection）进行训练，确保各专家模块获得稳定的初始化，避免路由器在早期随机探索中陷入局部最优。
- **第二阶段**：切换至路由器自主输出，通过端到端优化提升泛化性，使路由器学会在开放场景中做出合理的专家选择。

这一策略有效平衡了专家专项化的稳定性和路由器的泛化能力。消融实验表明，无监督的 Action MoE 性能明显下降（Table 6），验证了监督信号对专家解耦的关键作用。

### 模块协同与不可分割性

Vision MoE 和 Action MoE 并非孤立模块，而是形成协同效应：视觉侧的动态视图选择为动作侧提供更精准的场景表征，动作侧的技能专项化则充分利用这一表征实现行为解耦。消融实验证实，移除任一模块均导致性能显著下降——移除 Vision MoE 后 DS 从 74.22 降至 68.68，移除 Action MoE 后 DS 降至 67.31（Table 7），验证了两个模块的不可或缺性。

## 整体框架

DriveMoE 的整体设计遵循端到端视觉‑语言‑动作（VLA）范式，并在两个关键环节引入混合专家（MoE）机制以解决现有方法的瓶颈。其 pipeline 由五大模块串联构成，数据流从多视图图像输入到最终车辆控制指令输出，形成一条完整的闭环推理链路。

### 输入与骨干网络

系统接收环绕多视图图像序列作为原始输入。与现有 VLA 基线 **Drive‑π0** 仅使用两张连续前视图不同，DriveMoE 利用预训练的视觉‑语言模型 **Paligemma‑3b‑pt‑224** 作为骨干网络，从所有可用相机视图中提取视觉令牌，并同步理解导航文本指令。这一设计使得模型在输入阶段即具备多视图感知的潜力，但同时也引入了令牌冗余和计算开销的问题。

### 场景特化视觉混合专家（Scene‑Specialized Vision MoE）

为缓解多视图令牌冗余，DriveMoE 在视觉编码器之后插入 **Vision MoE** 模块。该模块由一个可学习的 **Vision Router** 驱动：路由器接收当前帧的前视图嵌入 $e_t^{\mathrm{front}}$ 和目标航点 $\pmb{g}_t$，输出所有相机视图的选择概率分布：

$${\pmb p}_t = \mathrm{Softmax}\left(R_{\mathrm{vision}}\left(e_t^{\mathrm{front}}, \pmb{g}_t\right)\right)$$

路由器据此动态选择 Top‑1 上下文相关视图（如侧视或后视），仅将该视图的令牌与前视图令牌一同送入后续融合层，从而在保留关键空间信息的同时大幅削减冗余计算。Vision Router 通过交叉熵损失进行监督训练：

$$\mathcal{L}_{\mathrm{Vision-Router}} = -\lambda_0 \sum_{v=1}^{N} \pmb{y}_t^v \log(\pmb{p}_t^v)$$

其中 $\pmb{y}_t^v$ 为基于规则标注的二值相机视图选择标签。选中的多视图令牌经 Projector 层融合为统一的视觉表征，供后续规划器使用。

### 技能特化动作混合专家（Skill‑Specialized Action MoE）

动作解码器是 DriveMoE 的第二个 MoE 改造点。基线 **Drive‑π0** 在条件流匹配（Conditional Flow Matching）轨迹解码器中使用单一的密集前馈网络（FFN），这种统一策略网络易受模式平均效应影响，在罕见驾驶行为（如紧急刹车、激进转弯）上表现欠佳。

DriveMoE 将解码器中的 FFN 替换为 **Action MoE** 层，其结构包含一个**共享专家**（shared expert）和 $K=6$ 个**非共享技能专家**（non‑shared skill experts）。**Action Router** 根据输入的驾驶上下文特征 $\mathbf{h}^{(\ell-1)}$ 计算专家选择概率：

$$r_k^{(\ell-1)} = \mathrm{Softmax}\left(R_{\mathrm{action}}(\mathbf{h}^{(\ell-1)})\right), \quad k \in \{1,2,\ldots,K\}$$

路由器采用稀疏激活机制，仅激活 Top‑3 专家参与前向计算。论文探索了两种 Action MoE 粒度：**令牌级**（Token‑Level）对轨迹序列中的每个时间步令牌独立路由，而**轨迹级**（Traj‑Level）则将整条轨迹的令牌序列平均池化后再送入路由器，沿轨迹维度进行统一的专家选择。实验表明，轨迹级路由显著优于令牌级（DS 73.88 vs 65.62），说明在轨迹层面进行行为解耦更符合驾驶技能的语义粒度。

Action Router 同样通过交叉熵损失进行监督训练，使用基于场景标注的驾驶技能标签 $y_k$：

$$\mathcal{L}_{\mathrm{Action-Router}} = -y_k \log(r_k)$$

总动作损失为流匹配轨迹损失与路由器损失的加权组合：

$$\mathcal{L}_{\mathrm{Action}} = \lambda_1 \mathcal{L}_{\mathrm{FM}} + \lambda_2 \mathcal{L}_{\mathrm{Action-Router}}$$

### 条件流匹配规划器与输出

融合后的视觉表征与导航指令共同输入到基于条件流匹配的轨迹 Transformer 中。该规划器以去噪方式建模未来轨迹的条件概率分布 $p(\mathbf{A}_t \mid \mathbf{o}_t)$，其核心损失函数为：

$$L^\tau(\theta) = \mathbb{E}_{p(\mathbf{A}_t \mid \mathbf{o}_t), q(\mathbf{A}_t^\tau \mid \mathbf{A}_t)} \left\| \mathbf{v}_\theta\big(\mathbf{A}_t^\tau, \mathbf{o}_t\big) - \mathbf{u}\big(\mathbf{A}_t^\tau \mid \mathbf{A}_t\big) \right\|^2$$

通过使网络输出的向量场 $\mathbf{v}_\theta$ 逼近真实方向 $\mathbf{u}$，规划器能够生成覆盖多种驾驶意图的多模态轨迹。最终，生成的未来路点序列由 **PID 控制器** 转换为底层车辆控制命令（油门、刹车、转向），完成从感知到控制的完整闭环。

### 两阶段训练策略

为稳定 MoE 路由器的学习，DriveMoE 采用两阶段训练：第一阶段使用基于规则的**真实标签**（ground‑truth expert assignment）强制指定专家选择，使各专家模块充分收敛；第二阶段切换至路由器自主输出，并通过上述监督损失进行微调，以提升模型的泛化能力。消融实验证实，移除任一 MoE 模块均导致性能显著下降（Vision MoE 移除后 DS 从 74.22 降至 68.68；Action MoE 移除后 DS 降至 67.31），验证了视觉‑动作双重专项化架构的必要性。

> **注意**：以上框架描述基于论文提供的分析与证据，公式编号与原文一致。关于真实世界部署的泛化性、无监督视图选择等开放问题，论文尚未给出明确解决方案，需进一步研究验证。

### 补充图表

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/002_Figure_2.jpg]]
*Figure 2: Framework of DriveMoE. Our proposed framework comprises two main Mixture-of-Experts (MoE) modules tailored for endto-end autonomous driving. The Scene-Specialized Vision MoE dynamically selects relevant camera views based on real-time driving contexts, efficiently reducing visual redundancy. Subsequently, selected views are fused into a unified representation by projector layers. The Skill-Specialized Action MoE, integrated within a flow-matching planner, activates expert controllers specifically optimized for distinct driving behaviors such as merging, overtaking, emergency braking, yielding, and responding to traffic signs. This dual MoE structure enhances computational efficiency, adapta...*

## 核心模块与公式推导

### 整体架构：双重混合专家设计

DriveMoE 在 VLA 端到端自动驾驶框架中引入两个互补的混合专家模块，分别针对视觉感知与动作规划中的核心瓶颈。整体架构如 Figure 2 所示：**场景特化视觉混合专家** 负责动态选择上下文相关的相机视图以降低令牌冗余；**技能特化动作混合专家** 集成于条件流匹配规划器中，对不同的驾驶行为激活不同的专家模块，实现行为解耦。

---

### 场景特化视觉混合专家

现有 VLA 方法通常将所有环视图像送入视觉编码器，导致大量冗余视觉令牌和计算开销。Vision MoE 的核心思想是：**借鉴人类驾驶员选择性关注关键视野的机制，通过可学习的路由器动态选择最相关的相机视图**。

#### Vision Router 概率分布

给定当前时刻的前视图嵌入 $e_t^{\mathrm{front}}$ 和目标航点 ${\pmb g}_t$，Vision Router $R_{\mathrm{vision}}$ 输出所有 $N$ 个相机视图的选择概率分布：

$${\pmb p}_t = \mathrm{Softmax}\left(R_{\mathrm{vision}}\left(e_t^{\mathrm{front}}, {\pmb g}_t\right)\right)$$

其中 ${\pmb p}_t \in \mathbb{R}^N$ 表示每个相机视图被选中的概率。推理时选择 Top-1 视图作为前视图的补充，形成精简的多视图输入。

#### Vision Router 监督损失

为训练路由器做出合理的视图选择，使用基于规则的二值标注 ${\pmb y}_t^v$（指示视图 $v$ 是否与当前驾驶场景相关），通过交叉熵损失进行监督：

$$\mathcal{L}_{\mathrm{Vision-Router}} = -\lambda_0 \sum_{v=1}^{N} {\pmb y}_t^v \log({\pmb p}_t^v)$$

该损失引导路由器学习场景感知的视图选择策略，使模型从“固定全视图”转向“动态上下文视图”。

---

### 技能特化动作混合专家

传统统一策略网络倾向于对常见驾驶行为产生模式平均效应，难以处理紧急刹车、激进转弯等罕见但关键的场景。Action MoE 将轨迹解码器中的密集前馈网络替换为 MoE 层，包含 **1 个共享专家** 和 **$K$ 个非共享技能专家**，由 Action Router 动态激活 Top-3 专家。

#### 令牌级 Action MoE

对于轨迹序列中第 $\ell$ 层的隐藏状态 ${\bf h}^{(\ell-1)}$，Action Router $R_{\mathrm{action}}$ 输出专家选择概率：

$$r_k^{(\ell-1)} = \mathrm{Softmax}\left(R_{\mathrm{action}}\left({\bf h}^{(\ell-1)}\right)\right), \quad k \in \{1, 2, \ldots, K\}$$

令牌级 MoE 层的输出为非共享专家输出的加权和与共享专家输出之和：

$${\pmb h}^{(\ell)} = \sum_{k=1}^{K} {\pmb r}_k^{(\ell-1)} {\pmb y}_k^{(\ell-1)} + \sum_{m=1}^{M} {\pmb y}_m^{(\ell-1)}$$

其中 ${\pmb y}_k^{(\ell-1)}$ 为第 $k$ 个非共享专家的输出，${\pmb y}_m^{(\ell-1)}$ 为第 $m$ 个共享专家的输出。

#### 轨迹级 Action MoE

与令牌级不同，轨迹级 Action MoE **先将整个轨迹序列的令牌取平均，再送入路由器**，在轨迹维度上进行专家选择。这使整个轨迹共享同一组专家激活，更符合“一个驾驶行为对应整条轨迹”的语义。

#### 动作路由器损失与总损失

使用驾驶技能标签 $y_k$（基于场景标注）对 Action Router 进行监督：

$$\mathcal{L}_{\mathrm{Action-Router}} = -y_k \log(r_k)$$

动作模块的总损失为流匹配轨迹损失与路由器损失的加权组合：

$$\mathcal{L}_{\mathrm{Action}} = \lambda_1 \mathcal{L}_{\mathrm{FM}} + \lambda_2 \mathcal{L}_{\mathrm{Action-Router}}$$

其中 $\mathcal{L}_{\mathrm{FM}}$ 为条件流匹配损失（详见附录），用于学习轨迹的条件概率分布。

---

### 条件流匹配规划器

DriveMoE 采用条件流匹配作为轨迹生成的核心机制。给定观测 ${\bf o}_t$，目标是学习从简单先验分布到真实轨迹分布 $p({\bf A}_t \mid {\bf o}_t)$ 的连续变换。流匹配损失定义为：

$$L^{\tau}(\theta) = \mathbb{E}_{p({\bf A}_t \mid {\bf o}_t), q({\bf A}_t^{\tau} \mid {\bf A}_t)} \left\| {\bf v}_{\theta}\big({\bf A}_t^{\tau}, {\bf o}_t\big) - {\bf u}\big({\bf A}_t^{\tau} \mid {\bf A}_t\big) \right\|^2$$

其中 ${\bf A}_t^{\tau}$ 为时间 $\tau$ 处的噪声轨迹，${\bf v}_{\theta}$ 为网络预测的向量场，${\bf u}$ 为从噪声轨迹指向真实轨迹的真实方向。该损失使网络学会从噪声逐步去噪生成合理的未来轨迹分布，天然支持多模态行为建模。

---

### 两阶段训练策略

为确保 MoE 路由器的稳定训练，DriveMoE 采用两阶段策略：

- **第一阶段**：使用真实标签（规则标注的视图选择标签和场景技能标签）强制路由器输出正确的专家选择，稳定专家模块的专项化学习。
- **第二阶段**：切换至路由器自身输出进行端到端微调，提升模型在未见场景中的泛化能力。

该策略在消融实验中验证了必要性：无监督的动态视图选择（Table 3, Exp 2 vs Exp 9）导致 DS 从 74.22 降至 68.68，证实监督信号对路由器训练的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/003_Figure_3.jpg]]
*Figure 3: The Scene-Specialized Vision Mixture-of-Experts*

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/004_Figure_4.jpg]]
*Figure 4: Token-Level Skill-Specialized Action Mixture-of-Experts*

## 实验与分析

### 核心瓶颈与实验设计逻辑

DriveMoE 旨在解决现有 VLA 端到端自动驾驶模型的两大瓶颈：（1）多视图视觉处理导致令牌冗余和巨大计算开销，收敛困难；（2）统一策略网络偏向常见驾驶场景，难以有效处理罕见但关键的驾驶行为（如紧急刹车、激进转弯），产生模式平均效应。实验设计围绕两个核心因果旋钮展开验证：视觉侧的 **Vision MoE** 是否通过动态视图选择减少了冗余并提升了感知效率，动作侧的 **Action MoE** 是否通过技能解耦避免了模式平均。

所有实验均在 Bench2Drive 官方 220 条路线上进行闭环评测，结果取三次运行平均，且所有方法使用相同的 PID 控制器以保证公平比较。基线方法均使用官方提供的训练数据（1000 clips，950 训练/50 验证）。

### 主实验结果：Bench2Drive 闭环评测

在 Bench2Drive 闭环评测中，DriveMoE（Traj-Level）达到 **Driving Score (DS) 74.22**，**Success Rate (SR) 48.64%**，相比基线 Drive-π0（DS 55.85，SR 30.00%）分别提升 **+18.37** 和 **+18.64 个百分点**（Table 2）。DS 提升幅度达 32.9%，SR 提升幅度达 62.1%，验证了双 MoE 架构的有效性。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/007_Table_2.jpg]]
*Table 2: Results on the Bench2Drive Benchmark(Closed-Loop and Open-Loop). * denotes expert feature distillation*

与先前 SOTA 方法对比，DriveMoE 同样展现出显著优势。TCP-traj\*（Wu et al., NeurIPS 2022）DS 为 62.85、SR 为 37.27%；AD-MLP（Zhai et al., ArXiv 2023）DS 为 48.56、SR 为 21.82%；VAD（Jiang et al., ICCV 2023）DS 为 48.59、SR 为 20.00%；UniAD-Base（Hu et al., CVPR 2023）DS 为 56.08、SR 为 32.73%；ThinkTwice\*（Jia et al., CVPR 2023）DS 为 64.72、SR 为 38.18%；DriveAdapter\*（Jia et al., ICCV 2023）DS 为 65.05、SR 为 39.09%；DriveTrans（Xu et al., ICLR 2025）DS 为 66.37、SR 为 40.91%；DiffAD（Zhang et al., ArXiv 2025）DS 为 68.68、SR 为 42.45%；Raw2Drive（Yang et al., NeurIPS 2025）DS 为 70.45、SR 为 45.45%。DriveMoE 在所有指标上均达到最优。

### 多能力评测：罕见行为的显著提升

Table 1 展示了 Bench2Drive 多能力评测结果。DriveMoE（Traj-Level）的 **Mean Ability 达到 47.91%**，相比 Drive-π0（33.37%）提升 **+14.54 个百分点**。尤其值得关注的是，在 **Merging、Emergency Brake** 等罕见但关键的驾驶行为上，DriveMoE 相比基线有大幅提升。这直接验证了 Action MoE 通过技能解耦避免模式平均效应的核心设计动机——统一策略网络在这些低频行为上表现不佳，而技能特化专家能够针对特定驾驶意图进行专项优化。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/006_Table_1.jpg]]
*Table 1: Performance on Bench2Drive Multi-Ability Benchmark. *: expert feature distillation*

Token-Level DriveMoE 的 Mean Ability 为 40.83%，虽优于基线但明显低于 Traj-Level（47.91%），初步表明轨迹级路由更适合行为解耦。

### Vision MoE 消融：动态视图选择的关键作用

Table 3 系统消融了相机视图组合与监督信号的影响。基线配置（Exp 1，仅使用两张连续前视图）DS 为 55.85、SR 为 30.00%。逐步增加固定视图（Exp 2–6）可带来一定提升，但增长有限。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/008_Table_3.jpg]]
*Table 3: Ablation study on Vision MoE. Compare different camera view combinations and supervision signals. F , F L, F R, and B indicate the front, front-left, front-right, and back views, respectively, while BL and BR represent the back-left and back-right views. Fixed View means selecting a specific view. Dynamic View refers to the camera view dynamically selected by the vision router as the top-1 relevant view according to scene context. Exp 1 denotes our baseline Drive-π0, which models surrounding agents’ velocities from two consecutive front-view images, and Exp 9 denotes DriveMoE, which adds a dynamically selected view with explicit supervision to enhance perception learning. Memory is evaluate...*

关键突破出现在动态视图选择：**动态选择+监督（Exp 9）达到 DS 74.22、SR 48.64%**，相比仅前视图基线 DS 提升 18.37，成功率提升 62%。即使不加监督信号（Exp 8），动态选择仍优于固定视图方案，表明 Vision Router 能够自主学习上下文相关的视图选择策略。监督信号的引入进一步稳定和提升了路由器的选择质量。

值得注意的是，仅增加一张动态选择的额外视图（从 2 视图到 3 视图）就带来了大幅性能提升，验证了“场景特化视图选择”比“简单堆叠所有视图”更高效——减少了令牌冗余，降低了计算开销，同时保留了关键上下文信息。

### Action MoE 消融：轨迹级路由与专家配置

**令牌级 vs 轨迹级路由**（Table 5）：Traj-Level Action MoE 的 DS 为 73.88、SR 为 48.64%，显著优于 Token-Level 的 DS 65.62、SR 32.27%。这一差异源于两种路由粒度的本质区别：Token-Level 对每个时间步令牌独立选择专家，关注短时域依赖但缺乏全局行为一致性；Traj-Level 对整个轨迹序列进行统一路由，能够捕捉完整的驾驶意图，更适合技能级别的行为解耦。

**专家数量与监督影响**（Table 6）：在 6 个非共享技能专家+监督的配置下（Exp 2）达到最佳 DS 74.22。移除监督信号后性能下降，验证了技能标签对路由器训练的指导价值。专家数量过少（如 3 个）导致技能划分不够精细，过多（如 9 个）可能引入冗余或训练不稳定。

### 模块不可或缺性验证

Table 7 的模块移除实验直接验证了两个 MoE 模块的不可或缺性。完整模型 DS 为 74.22、SR 为 48.64%；**移除 Vision MoE** 后降至 DS 68.68、SR 42.45%（DS 下降 5.54）；**移除 Action MoE** 后降至 DS 67.31、SR 40.56%（DS 下降 6.91）。两个模块的移除均导致性能显著下降，且 Action MoE 的移除带来的损失略大于 Vision MoE，暗示行为解耦在整体框架中扮演着更为关键的角色。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/011_Table_7.jpg]]
*Table 7: Drive-π0 vs DriveMoE. Evaluate the Vision MoE and Action MoE. ”w/o” denotes removing the respective modules*

### nuScenes 开环规划验证

在 nuScenes 开环规划评测中（Table 9），DriveMoE 的 L2 Average 为 0.74m、Collision Avg 为 0.17%，相比 Drive-π0（0.78m / 0.24%）均有改善。虽然开环评测的提升幅度不如闭环显著（这是开环评测的固有局限性），但结果仍表明 DriveMoE 的架构设计在不同数据集和评测设定下具有一致的增益。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/012_Table_9.jpg]]
*Table 9: Open-loop planning performance in nuScenes*

### 模型规模与推理成本

Table 10 对比了模型规模与推理成本。DriveMoE 在引入 MoE 架构后，参数量相比基线有所增加，但由于 Vision MoE 的动态视图选择减少了实际处理的视觉令牌数量，推理时延和计算开销的上涨幅度有限。具体数值需对照 Table 10 确认（此处基于分析推断，建议人工核实精确的参数量和推理时间数据）。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/013_Table_10.jpg]]
*Table 10: Comparison of model scale and inference cost*

### 路由器准确率分析

Table 4 报告了 Vision Router 和 Action Router 在 Bench2Drive-Base 验证集上的准确率。两个路由器的准确率均达到较高水平，表明：（1）Vision Router 能够有效学习场景上下文与关键相机视图之间的映射关系；（2）Action Router 能够准确识别驾驶技能类型。路由器的可靠性是 MoE 架构有效性的前提——如果路由器频繁做出错误选择，专家模块的专项化优势将无法发挥。

### 失败模式与局限性讨论

尽管 DriveMoE 取得了显著的性能提升，但需注意以下局限：（1）所有实验均在 CARLA 仿真环境中完成，尚未在真实世界自动驾驶数据集或实车部署中验证；（2）相机视图选择依赖人工标注规则，虽然标注成本低（每帧仅需标注一个最相关视图），但仍存在覆盖不全或主观偏差的风险；（3）技能定义和场景划分基于 Bench2Drive 预设（Table 8），可能无法覆盖所有开放道路驾驶行为；（4）两阶段训练策略（第一阶段强制使用真实标签专家，第二阶段切换至路由器输出）增加了训练复杂度。这些局限性指向了未来工作的方向：自监督视图选择、更大规模数据集验证、模型蒸馏部署、以及更灵活的技能解耦与持续学习机制。

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/014_Table_8.jpg]]
*Table 8: Skill Set & Scenarios*

### 补充图表

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/009_Table_5.jpg]]
*Table 5: Token vs Trajectory Level Action MoE*

![[assets/figures/papers/paper_list_l2384_https_arxiv_org_abs_2505_16278/figures/010_Table_6.jpg]]
*Table 6: Ablation Study in Action MoE. Compare various configurations of non-share expert numbers within Action MoE*

## 方法谱系与知识库定位

### 1. 基线谱系与核心差异

DriveMoE 建立在 Vision-Language-Action (VLA) 端到端自动驾驶范式之上，其直接基线 **Drive-π0** 是将具身智能领域的 VLA 架构迁移至自动驾驶的初步尝试。Drive-π0 的核心设计包括：仅使用两张连续前视图作为视觉输入，通过单一密集前馈网络（FFN）的 flow-matching 轨迹解码器生成未来轨迹。这一设计存在两个结构性瓶颈：**视觉令牌冗余**（仅依赖前视图导致感知视野受限，而直接引入多视图又会带来计算开销爆炸）和**行为模式平均**（统一策略网络倾向于拟合常见驾驶场景，在罕见但关键的驾驶行为上表现不佳）。

DriveMoE 的关键改进在于将混合专家（MoE）架构引入视觉和动作两个层面，实现双重专项化：

| 设计维度 | Drive-π0 (基线) | DriveMoE (本文) |
|---------|----------------|----------------|
| 多视图视觉输入 | 仅两张连续前视图 | Vision MoE 动态选择 Top-1 上下文相关相机视图 |
| 动作解码器 | 单一密集 FFN | Action MoE（1 共享专家 + 6 非共享技能专家，Top-3 激活） |
| 训练策略 | 标准单阶段训练 | 两阶段训练（先强制真值标签稳定训练，后切换路由器输出） |

在更广泛的端到端自动驾驶方法谱系中，DriveMoE 的定位如下：

- **传统端到端方法**：**UniAD-Base** (Hu et al., CVPR 2023)、**VAD** (Jiang et al., ICCV 2023)、**TCP-traj\*** (Wu et al., NeurIPS 2022) 等方法在 Bench2Drive 闭环评测上的 Driving Score 普遍在 30–55 区间，远低于 DriveMoE 的 74.22。这些方法通常采用单一策略头处理所有场景，缺乏对罕见驾驶行为的专项优化。
- **扩散/Transformer 方法**：**DiffAD** (Zhang et al., ArXiv 2025)、**DriveTrans** (Xu et al., ICLR 2025) 等引入扩散模型或 Transformer 架构，但未显式解决视觉冗余和行为解耦问题。
- **VLA 范式方法**：Drive-π0 是首个将 VLA 范式应用于端到端自动驾驶的工作，DriveMoE 在此基础上通过 MoE 架构实现了显著提升（DS +18.37，SR +18.64%）。

### 2. 适用边界

**适用场景**：
- 多视图输入的端到端自动驾驶系统，尤其是需要动态选择关键相机视图以减少令牌冗余的场景。
- 需要处理多样化驾驶行为（如紧急刹车、激进转弯、汇入车流）的复杂交通环境。
- 基于 CARLA 仿真器的闭环评测环境，尤其是 Bench2Drive 基准测试。

**不适用或需谨慎的场景**：
- 仅依赖单视图输入的简单驾驶场景（Vision MoE 的动态选择优势无法充分发挥）。
- 对推理时延有极端严格要求的实时部署场景（MoE 架构相比简单基线仍有一定计算开销，见表 10 的模型规模与推理成本对比）。
- 超出 Bench2Drive 预设技能划分范围的开放道路驾驶行为（技能定义和场景划分的泛化性未经验证）。

### 3. 局限与开放问题

**已知局限**（来自论文及分析验证）：

1. **仿真环境限制**：目前仅在 CARLA 仿真环境中验证，未在真实世界自动驾驶数据集或实车部署中测试。仿真到现实的迁移（Sim-to-Real）能力尚未得到验证。
2. **标注依赖性**：相机视图选择依赖人工标注规则（基于场景的相机视图选择标签），虽然标注成本相对较低，但仍存在覆盖不全或主观偏差的风险。动作路由器同样依赖驾驶技能标签进行监督训练。
3. **训练复杂度**：两阶段训练策略增加了训练流程的复杂度，且需要额外的技能标签和视图选择标签。
4. **技能覆盖范围**：技能定义和场景划分基于 Bench2Drive 预设，可能无法覆盖所有开放道路驾驶行为，尤其是长尾分布中的极端情况。
5. **推理开销**：虽然相比基线提升有限，但 MoE 架构的推理时延和计算开销仍高于简单密集网络基线（见表 10）。

**开放问题**：

1. **无监督/自监督视图选择**：能否通过自监督学习或强化学习实现相机视图选择的完全自主化，彻底消除对人工标注的依赖？当前 Vision Router 的交叉熵损失需要二值相机视图选择标注，若能通过对比学习或基于任务奖励的强化学习来训练路由器，将大幅降低数据准备成本。

2. **更大规模数据集的泛化性**：MoE 架构在更大规模的驾驶数据集（如 nuPlan、Waymo Open Dataset）上是否能保持性能优势？Bench2Drive 仅包含 1000 个 clips（950 训练/50 验证），在更大数据规模下，专家模块是否会出现负载不均衡或专家坍缩问题需要进一步验证。

3. **轻量化部署**：如何将 DriveMoE 蒸馏为轻量级部署模型，以满足车规级实时性要求？可能的路径包括专家剪枝、知识蒸馏到单一密集网络、或通过量化技术减少推理成本。

4. **真实世界的安全性与泛化性**：在真实物理世界自动驾驶中，Vision Router 的泛化能力和安全性如何保证？动态视图选择在面对未见过的场景（如极端天气、传感器故障）时是否会产生错误的路由决策，导致关键视野丢失？

5. **更灵活的技能解耦**：是否存在更优的技能解耦方式，使得专家模块可以动态增减或持续学习新技能？当前固定 6 个非共享技能专家的设计（见表 6 消融实验）可能无法适应开放世界中不断出现的新驾驶行为，在线学习或终身学习机制值得探索。

6. **跨具身迁移**：DriveMoE 的双重 MoE 设计（视觉专项化 + 动作专项化）是否可泛化到其他具身智能任务（如机器人导航、机械臂操控）？Vision MoE 的“动态选择感知视角”和 Action MoE 的“技能解耦”思想在更广泛的 Embodied AI 场景中具有潜在的迁移价值，但需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/DriveMoE_Mixture_of_Experts_for_Vision_Language_Action_Model_in_End_to_End_Autonomous_Driving.pdf]]
