---
title: "TeamHOI: Learning a Unified Policy for Cooperative Human-Object Interactions with Any Team Size"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interactions_with_Any_Team_Size.pdf
project_link: https://splionar.github.io/TeamHOI
code_link: null
aliases:
- TeamHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入Transformer架构和队友令牌（teammate tokens）实现可变团队规模的显式感知与协调，并通过掩码对抗运动先验（Masked AMP）策略从单人参考运动中扩展协作行为多样性，辅以主轴覆盖队形奖励引导分布式稳定协作。
primary_logic: 利用Transformer策略中的交叉注意力机制处理任意数量的队友状态，结合掩码AMP策略从单人参考运动中合成多样化的协作行为，能够在单一统一策略下实现跨团队规模和物体几何形状的高效协作搬运。
claims:
- 在合作搬运任务中，统一策略在2至8个智能体上均取得超过97.5%的成功率，而基线方法（如CooHOI*-2在8智能体上仅为10.1%）无法泛化到不同团队规模。
- 在重载（5倍桌面重量）条件下，只有本文方法在8智能体上实现了有效协作（成功率81.1%），而CooHOI*-8仅为4.1%。
- 消融实验证实掩码AMP显著提升了举升阶段成功率，并使得手-物交互行为更加多样化。
- 主轴覆盖队形奖励使智能体形成沿物体主轴对齐的稳定队形，有利于自然行走。
---

# TeamHOI: Learning a Unified Policy for Cooperative Human-Object Interactions with Any Team Size

> [!tip] 核心洞察
> 利用Transformer策略中的交叉注意力机制处理任意数量的队友状态，结合掩码AMP策略从单人参考运动中合成多样化的协作行为，能够在单一统一策略下实现跨团队规模和物体几何形状的高效协作搬运。

| 字段 | 内容 |
|------|------|
| 中文题名 | TeamHOI：学习适用于任意团队规模的协作人物体交互统一策略 |
| 英文题名 | TeamHOI: Learning a Unified Policy for Cooperative Human-Object Interactions with Any Team Size |
| 会议/期刊 | CVPR 2026 |
| Links | [Project](https://splionar.github.io/TeamHOI) · [paper](https://arxiv.org/abs/2603.07988) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TeamHOI |
| Dataset | cooperative carrying, cooperative carrying heavy weight 5x |

> [!tip] 效果简介
> - cooperative carrying (2 agents) 上，Success Rate (%) 99.1 vs 97.5 (CooHOI*-2) (+1.6)。
> - cooperative carrying (4 agents) 上，Success Rate (%) 99.2 vs 94.5 (CooHOI*-4) (+4.7)。
> - cooperative carrying (8 agents) 上，Success Rate (%) 97.5 vs 42.2 (CooHOI*-8) (+55.3)。

## 概要

**核心问题**：在物理仿真环境中实现多智能体协作人物体交互（Human-Object Interaction, HOI）时，现有方法面临两个根本性瓶颈。其一，基于MLP的策略架构要求固定维度的输入，导致策略无法泛化到不同团队规模，每个团队规模都需要独立训练。其二，多智能体参考运动数据的匮乏限制了协作行为的多样性——单人运动捕捉数据丰富，但多人协作的参考运动极为稀缺。

**核心洞见**：TeamHOI通过两个关键设计突破上述瓶颈。在策略架构层面，引入Transformer并利用队友令牌（teammate tokens）实现可变团队规模的显式感知与协调——交叉注意力机制使每个智能体能够动态关注任意数量的队友状态，从而在单一统一策略下支持2至8个智能体的协作。在行为多样性层面，提出掩码对抗运动先验（Masked AMP）策略，仅使用单人参考运动数据：在智能体与物体交互时，掩码掉接触物体的身体部位（如手部），仅对非交互部位施加动作真实性约束，从而释放交互部位的行为多样性，使策略能够自主合成多样化的协作搬运行为。

**方法定位**：TeamHOI属于物理仿真驱动的多智能体强化学习方法，其技术谱系可追溯至AMP（Adversarial Motion Prior）框架和Transformer策略架构。与基线方法**CooHOI***（基于CooHOI改进，使用预定义接触点和无队友令牌的Transformer）相比，TeamHOI的核心改进在于：(1) 用交叉注意力替代自注意力，实现显式的队友状态感知；(2) 用掩码AMP替代全身AMP，从单人参考运动中扩展协作行为；(3) 引入主轴覆盖队形奖励，引导分布式稳定协作。

**主要结果**：在合作搬运任务上，TeamHOI统一策略在2至8个智能体上均取得超过97.5%的成功率，而CooHOI*-8在8智能体上仅为42.2%（Table 1）。在重载条件下（5倍桌面重量），TeamHOI在8智能体上成功率达81.1%，而CooHOI*-8仅为4.1%。消融实验证实掩码AMP显著提升了举升阶段成功率并促进多样化手-物交互（Figure 5），主轴覆盖奖励使智能体形成沿物体主轴对齐的稳定队形（Figure 6）。此外，统一策略展现出对未见过的物体尺寸和团队规模的零样本泛化能力（Table 4, Figure 9）。

物理仿真环境中的人形智能体协作操控是具身智能领域的核心挑战之一。随着任务复杂度提升，多智能体系统需要协调各自的运动与交互行为，共同完成单人无法实现的搬运、组装等任务。基于强化学习的物理角色动画方法近年来取得了显著进展，但在多智能体协作人物体交互（Human-Object Interaction, HOI）方面仍面临两个关键瓶颈。

**固定团队规模的架构限制。** 现有方法普遍采用基于MLP的策略网络，其输入维度固定，导致策略只能适配特定数量的智能体。以基线方法CooHOI为代表的工作，虽然通过预定义接触点和隐式物体共享动态实现了一定程度的协作，但策略无法感知队友的显式状态，缺乏对协作关系的直接建模。这使得策略在团队规模变化时需要重新训练，严重限制了可扩展性。当团队规模从4人扩展到8人时，CooHOI的成功率从94.5%骤降至42.2%，而在重载场景下更是跌至4.1%，暴露出固定架构在协调大量智能体时的根本性缺陷。

**协作行为多样性的数据匮乏。** 基于对抗运动先验（Adversarial Motion Prior, AMP）的方法依赖参考运动数据来引导策略生成自然的人体动作。然而，多智能体协作的参考运动数据极为稀缺，现有数据集大多仅包含单人动作。标准全身AMP要求策略模仿参考运动的所有身体部位，这在协作搬运场景中会产生矛盾：智能体的手部需要与物体接触并施加力量，而参考运动中的手部动作往往是自由的，两者之间的冲突导致策略难以学习有效的交互行为，也无法产生多样化的手-物交互模式。

上述两个瓶颈共同指向一个核心问题：**如何在无需多人参考运动数据的前提下，构建一个能够适应任意团队规模、且能产生多样化协作行为的统一策略框架？** 本文提出的TeamHOI正是针对这一问题，通过引入Transformer架构实现可变团队规模的显式队友感知，并设计掩码AMP策略从单人参考运动中扩展协作行为多样性，为多智能体协作HOI提供了一条可扩展的技术路径。

## 核心方法与创新机理

TeamHOI 的核心创新围绕三个关键 **changed slots** 展开，分别针对现有物理仿真多智能体协作方法中“固定团队规模”和“协作行为多样性不足”两大瓶颈，形成了一套可扩展的统一策略框架。

### 1. 基于 Transformer 与队友令牌的可扩展策略架构

**瓶颈**：基线方法（如 **CooHOI**）采用基于 MLP 的策略网络，其输入维度固定，限制了策略只能应用于特定团队规模；同时，CooHOI 隐式地依赖物体共享动态进行智能体间通信，缺乏对队友状态的显式感知，导致协作的自适应性和可扩展性不足。

**创新**：TeamHOI 将策略网络替换为 **Transformer 架构**，并引入 **队友令牌（teammate tokens）** 机制。具体而言，每个智能体的观察被编码为“本体感知令牌”，而队友的状态（位置、朝向、相对角度）则被编码为额外的“队友令牌”。Transformer 编码器通过交替的自注意力和与队友令牌的交叉注意力层，使当前智能体能够显式地关注任意数量的队友状态，从而突破了 MLP 策略对固定输入维度的限制，实现了对可变团队规模的统一支持（Section 3.2，Figure 2）。

这一架构设计使得单个统一策略能够在 2 至 8 个智能体的合作搬运任务中均取得超过 97.5% 的成功率，而基线方法 CooHOI*-8 在 8 智能体场景下仅为 42.2%（Table 1）。

### 2. 掩码 AMP：从单人参考运动中扩展协作行为多样性

**瓶颈**：现有基于动作先验（AMP）的方法依赖全身参考运动数据，但多智能体协作的多样化参考运动数据极为稀缺，限制了策略学习丰富协作行为的能力。

**创新**：TeamHOI 提出 **掩码对抗运动先验（Masked AMP）** 策略。该方法仅使用 **单人参考运动数据**，但在 AMP 监督过程中，根据智能体与物体的交互程度动态地掩码掉与物体接触的身体部位（如手部）。具体实现上，维护两个鉴别器：全身鉴别器在非交互期间评估动作真实性，掩码鉴别器则在交互期间忽略被掩码部位，允许策略在接触物体时探索多样化的手-物交互行为。最终风格奖励由交互指示器 $\sigma(\alpha_t)$ 混合两者：

$$r_{t}^{\mathrm{style}} = \sigma(\alpha_{t}) r_{t}^{\mathrm{mask}} + (1-\sigma(\alpha_{t})) r_{t}^{\mathrm{full}}$$

**证据强度**：消融实验（Figure 5，Section 4.3）证实，掩码 AMP 显著提升了举升阶段的成功率，并使手-物交互行为更加多样化。在重载（5 倍桌面重量）条件下，仅 TeamHOI 在 8 智能体上实现了有效协作（成功率 81.1%），而 CooHOI*-8 仅为 4.1%（Table 1）。

### 3. 主轴覆盖队形奖励：引导分布式稳定协作

**瓶颈**：基线方法依赖预定义的手部目标接触点来协调队形，缺乏对团队规模和物体几何形状的自适应能力。

**创新**：TeamHOI 设计了 **不依赖团队数量和物体形状的队形奖励**，由两部分加权组成：

- **角度分散奖励**（$r_{\mathrm{ang}}$）：鼓励智能体围绕桌面中心均匀分布，使相邻智能体之间的角度差接近 $2\pi/m$（$m$ 为智能体数量）。
- **主轴覆盖奖励**（$r_{\mathrm{cov}}$）：衡量智能体支撑多边形沿物体两条主轴的覆盖程度，鼓励队形沿物体主轴对齐以提供稳定支撑。

最终队形奖励为 $r_{\mathrm{form}} = 0.25 r_{\mathrm{ang}} + 0.75 r_{\mathrm{cov}}$（Equation 7）。消融实验（Figure 6，Section 4.3）表明，加入主轴覆盖奖励后，智能体能够形成沿物体主轴对齐的稳定队形，从而有利于自然行走。

### 创新总结

上述三个 changed slots 形成了 TeamHOI 的核心创新链条：**Transformer + 队友令牌**解决了“可变团队规模”的可扩展性问题；**掩码 AMP** 解决了“协作行为多样性”的数据稀缺问题；**主轴覆盖队形奖励**则提供了不依赖预定义接触点的自适应协调机制。三者协同，使得单一统一策略能够在跨团队规模和物体几何形状的合作搬运任务中实现高效、稳定的协作。

TeamHOI 旨在学习一个统一的去中心化策略，使可变数量的仿人智能体能够协作搬运不同几何形状的物体。其核心瓶颈在于：传统基于 MLP 的策略架构要求固定维度的输入，无法直接扩展到任意团队规模；同时，现有方法（如 CooHOI）隐式依赖物体共享动态进行通信，缺乏对队友状态的显式感知，限制了协作的自适应性和可扩展性。

为突破这一瓶颈，TeamHOI 构建了一个基于 Transformer 的统一策略框架，其核心因果机制可概括为三点：

1. **可变团队规模的显式感知**：通过队友令牌（teammate tokens）将任意数量队友的状态编码为可变长度序列，利用交叉注意力机制实现可扩展的协调。
2. **从单人参考运动扩展协作行为多样性**：提出掩码对抗运动先验（Masked AMP）策略，在物体交互期间掩码接触部位，仅对非接触部位施加风格监督，从而从单人参考运动中合成多样化的协作行为。
3. **分布式稳定队形引导**：设计主轴覆盖队形奖励，引导智能体沿物体主轴对齐形成稳定支撑队形，无需预定义接触点。

### 整体 Pipeline 与模块关系

TeamHOI 的完整 pipeline 由以下核心模块串联构成（参见 Figure 2）：

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TeamHOI framework. A transformer-based policy network enables coordination between the observing agent (green humanoid) and its teammates (grey humanoids) through alternating self- and cross-attention layers. By training across diverse team-size environments, the framework learns a unified policy that works across different team configurations. To maintain motion realism and enhance skill diversity, a masked AMP strategy blends full-body and masked discriminators based on object interaction*

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **本体感知分词器** | 将智能体自身状态编码为令牌 | 自身本体感知状态（223维） | 本体感知令牌 |
| **队友令牌分词器** | 将队友状态编码为令牌序列 | 队友位置、朝向、相对角度 | 队友令牌序列 |
| **带交叉注意力的 Transformer 编码器** | 通过自注意力和交叉注意力融合自身与队友信息 | 本体感知令牌 + 队友令牌 | 更新后的嵌入表示 |
| **动作头 MLP** | 预测目标关节旋转 | Transformer 输出的嵌入 | PD 控制器的目标姿态 |
| **掩码 AMP 模块** | 提供风格奖励以保持动作自然性 | 策略生成的动作过渡 vs 参考动作过渡 | 混合风格奖励 $r_t^{\mathrm{style}}$ |

### 策略网络架构

策略网络采用 Transformer 架构，其关键设计在于**交替的自注意力和交叉注意力层**（Figure 2）。观察智能体（绿色人形）的本体感知令牌首先通过自注意力层进行内部特征融合，随后通过交叉注意力层关注所有队友令牌（灰色人形），从而显式感知队友的空间分布和状态。由于 Transformer 天然支持可变长度序列输入，该架构能够在单一策略参数下处理 2 至 8 个（乃至更多）智能体的协作场景，彻底消除了 MLP 策略的固定输入维度限制。

策略优化采用 PPO 算法，总奖励为任务奖励与风格奖励的加权和：
$$r_t = r_t^{\mathrm{task}} + \lambda_{\mathrm{AMP}} r_t^{\mathrm{style}}$$

### 掩码 AMP 策略

传统全身 AMP（Full-body AMP）使用单一鉴别器评估全身动作的真实性：
$$r_t^{\mathrm{style}} = -\log(1 - D_\phi(s, s'))$$

然而，在协作搬运场景中，手部与物体的接触行为在单人参考运动数据中并不存在，强制施加全身风格约束会抑制协作行为的多样性。TeamHOI 的**掩码 AMP** 策略引入两个鉴别器：

- **全身鉴别器**：在非交互期间评估全身动作真实性。
- **掩码鉴别器**：在交互期间掩码与物体接触的身体部位（如手部），仅对未接触部位施加风格监督。

两者的风格奖励根据交互程度 $\alpha_t$ 进行混合：
$$r_t^{\mathrm{style}} = \sigma(\alpha_t) r_t^{\mathrm{mask}} + (1 - \sigma(\alpha_t)) r_t^{\mathrm{full}}$$

这一设计使得策略在交互阶段能够自由探索多样化的手-物接触行为，同时在非交互阶段保持自然的人类运动模式。消融实验证实，掩码 AMP 显著提升了举升阶段的成功率，并促进了更加多样化的手-物交互行为（Figure 5）。

### 队形协调机制

为实现分布式稳定协作，TeamHOI 设计了不依赖团队数量和物体形状的队形奖励 $r_{\mathrm{form}}$，由两部分加权组成：
$$r_{\mathrm{form}} = 0.25 r_{\mathrm{ang}} + 0.75 r_{\mathrm{cov}}$$

- **角度分散奖励 $r_{\mathrm{ang}}$**：鼓励智能体围绕桌面中心均匀分布，避免拥挤在一侧导致失衡：
$$r_{\mathrm{ang}} = \exp\Bigl( - k_{\theta} \frac{1}{2} \bigl[ (\Delta \phi_{i}^{\mathrm{ccw}} - \frac{2\pi}{m})^{2} + (\Delta \phi_{i}^{\mathrm{cw}} - \frac{2\pi}{m})^{2} \bigr] \Bigr)$$

- **主轴覆盖奖励 $r_{\mathrm{cov}}$**：衡量支撑多边形沿物体两条主轴的覆盖程度（Figure 3），引导智能体沿物体主轴对齐形成稳定支撑：
$$g_{i} = \operatorname*{min}\left( \frac{\tilde{d}_{i}^{+}}{\ell_{i}^{+}}, \frac{\tilde{d}_{i}^{-}}{\ell_{i}^{-}} \right), \quad r_{\mathrm{cov}} = \frac{1}{2}(g_{1} + g_{2})$$

消融实验表明，加入主轴覆盖奖励后，智能体形成了沿物体主轴对齐的稳定队形，有利于自然行走（Figure 6）。

### 输入输出流总结

整体数据流为：仿真环境提供各智能体的本体感知状态和队友状态 → 分词器编码为令牌 → Transformer 编码器融合信息 → 动作头输出目标关节旋转 → PD 控制器驱动物理仿真。同时，掩码 AMP 模块根据交互程度提供风格奖励，队形奖励模块根据智能体空间分布提供协调信号，二者共同汇入总奖励函数指导 PPO 优化。

TeamHOI 的统一策略架构围绕三个核心设计展开：基于 Transformer 的可扩展协调网络、掩码对抗运动先验（Masked AMP）策略，以及不依赖团队规模的队形奖励机制。以下逐一解析各模块的公式定义与设计意图。

### 3.1 基础框架：AMP 风格奖励

TeamHOI 建立在对抗运动先验（Adversarial Motion Prior, AMP）框架之上。策略 $\pi$ 在每一步接收状态 $s$ 并输出动作 $a$，环境返回任务奖励 $r_t^{\mathrm{task}}$。为保持动作自然性，AMP 引入一个鉴别器 $D_\phi$，其风格奖励定义为：

$$r_{t}^{\mathrm{style}} = -\log(1 - D_{\phi}(s, s'))$$

其中 $(s, s')$ 表示连续两帧的状态转移。鉴别器通过二分类损失训练，区分参考运动数据中的真实转移与策略生成的转移：

$$\mathcal{L}_{D} = -\mathbb{E}_{(s,s')^{\mathrm{ref}}}[\log D_{\phi}(s,s')] - \mathbb{E}_{(s,s')^{\pi}}[\log(1-D_{\phi}(s,s'))]$$

策略优化的总奖励为任务奖励与风格奖励的加权和：

$$r_{t} = r_{t}^{\mathrm{task}} + \lambda_{\mathrm{AMP}} r_{t}^{\mathrm{style}}$$

策略通过 PPO 目标使用 $r_t$ 进行优化。

### 3.2 掩码 AMP：从单人参考运动扩展协作行为多样性

传统全身 AMP 要求策略模仿参考运动的所有身体部位，这严重限制了协作搬运中手-物交互的多样性——单人参考运动中不存在多人协同抓握的姿态。TeamHOI 提出**掩码 AMP（Masked AMP）** 策略来解决这一瓶颈。

核心思想是：根据智能体与物体的交互程度，动态混合全身鉴别器奖励与掩码鉴别器奖励。定义交互指示器 $\alpha_t$（与手-物接触程度相关），混合风格奖励为：

$$r_{t}^{\mathrm{style}} = \sigma(\alpha_{t}) r_{t}^{\mathrm{mask}} + (1-\sigma(\alpha_{t})) r_{t}^{\mathrm{full}}$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数，$r_{t}^{\mathrm{full}}$ 来自标准全身鉴别器，$r_{t}^{\mathrm{mask}}$ 来自掩码鉴别器——后者在计算时忽略与物体接触的身体部位（如手部），从而允许这些部位在任务奖励引导下自由探索多样化的交互姿态。

**设计意图**：在非交互阶段（如行走接近物体），全身鉴别器保持动作自然性；在交互阶段（如举升、搬运），掩码鉴别器释放手部约束，使策略能够合成单人参考运动中不存在的协作抓握行为。消融实验（Figure 5）证实，掩码 AMP 显著提升了举升阶段的成功率和手-物交互的多样性。

### 3.3 队形奖励：不依赖团队规模的分布式协调

为使任意数量的智能体自发形成稳定的协作队形，TeamHOI 设计了两个互补的队形奖励分量。

#### 3.3.1 角度分散奖励

角度分散奖励鼓励智能体围绕物体中心均匀分布。对于 $m$ 个智能体，定义每个智能体 $i$ 与其逆时针和顺时针相邻队友之间的角度差 $\Delta \phi_i^{\mathrm{ccw}}$ 和 $\Delta \phi_i^{\mathrm{cw}}$，理想角度间隔为 $2\pi/m$：

$$r_{\mathrm{ang}} = \exp\Bigl( - k_{\theta} \frac{1}{2} \bigl[ (\Delta \phi_{i}^{\mathrm{ccw}} - \frac{2\pi}{m})^{2} + (\Delta \phi_{i}^{\mathrm{cw}} - \frac{2\pi}{m})^{2} \bigr] \Bigr)$$

该奖励在智能体均匀环绕物体时达到最大值 1，且不依赖绝对位置，天然支持可变团队规模。

#### 3.3.2 主轴覆盖奖励

仅靠角度分散无法保证队形的稳定性——智能体可能均匀分布但未沿物体主轴对齐，导致行走时支撑不稳。主轴覆盖奖励衡量所有智能体手部构成的支撑多边形沿物体两个主轴的覆盖程度（Figure 3）：

$$g_{i} = \operatorname*{min}\left( \frac{\tilde{d}_{i}^{+}}{\ell_{i}^{+}}, \frac{\tilde{d}_{i}^{-}}{\ell_{i}^{-}} \right), \quad i \in \{1,2\}$$

$$r_{\mathrm{cov}} = \frac{1}{2}(g_{1} + g_{2})$$

其中 $\ell_i^+$ 和 $\ell_i^-$ 为物体沿主轴 $i$ 正负方向的半长度，$\tilde{d}_i^+$ 和 $\tilde{d}_i^-$ 为支撑多边形在该方向上的投影覆盖距离。$g_i$ 取正负方向覆盖比例的最小值，确保两侧均衡支撑。

#### 3.3.3 综合队形奖励

最终的队形奖励为两者的加权组合，主轴覆盖权重更高（0.75），以优先保证行走稳定性：

$$r_{\mathrm{form}} = 0.25 r_{\mathrm{ang}} + 0.75 r_{\mathrm{cov}}$$

消融实验（Figure 6）表明，加入主轴覆盖奖励后，智能体能够形成沿物体主轴对齐的稳定队形，有利于自然行走。

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/007_Figure_6.jpg]]
*Figure 6: Formation reward comparison. Adding principal-axes coverage reward produces stable formations aligned with the object’s principal axes, facilitating learned natural locomotion*

### 3.4 策略网络架构：Transformer 与队友令牌

为实现对任意数量队友的显式感知，TeamHOI 采用 Transformer 编码器作为策略网络主干（Figure 2）。观察智能体的本体感知状态（维度 223）经**本体感知分词器**编码为令牌；队友状态（位置、朝向、相对角度）经**队友令牌分词器**编码为队友令牌序列。Transformer 通过交替的自注意力和与队友令牌的交叉注意力层处理这些令牌，使观察智能体能够动态关注任意数量的队友状态，从根本上突破了 MLP 策略的固定输入维度限制。更新后的嵌入经**动作头 MLP** 预测目标关节旋转。

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/006_Figure_5.jpg]]
*Figure 5: Ablation on the masked AMP strategy. Comparison between models trained with and without masked AMP, showing improved task rewards and successful hand-object interactions when masking is applied*

## 实验与关键发现

### 实验设置概述

实验在IsaacGym物理仿真环境中进行，核心任务为**合作搬运**——多个仿人智能体需协同将一张桌子从起点搬运至目标位置。为验证方法的可扩展性，团队规模从2个智能体跨越至8个智能体，并在标准重量（1×）和重载（5×桌面重量）两种条件下进行测试。训练采用多阶段课程学习策略，总耗时约9.5天，所有定量结果均基于10,000次仿真回合取平均。

为公平比较，作者对基线方法**CooHOI**进行了大幅改进（记为**CooHOI\*-n**，n为团队规模），融入了掩码AMP和接触点导向奖励，使其具备基本的搬运能力。然而，基线仍受限于预定义的接触点和缺乏队友令牌，无法实现跨团队规模的泛化。

### 主要结果：统一策略的跨规模协作能力

Table 1展示了核心定量对比结果。TeamHOI使用**单一统一策略**在所有团队规模上均取得了超过97.5%的成功率，而CooHOI\*-n基线需为每个团队规模独立训练，且性能随规模增大急剧下降。

| 团队规模 | TeamHOI (SR%) | CooHOI\*-n (SR%) | 提升幅度 |
|---------|---------------|------------------|---------|
| 2智能体  | 99.1          | 97.5             | +1.6    |
| 4智能体  | 99.2          | 94.5             | +4.7    |
| 8智能体  | 97.5          | 42.2             | +55.3   |

在8智能体场景中，CooHOI\*-8的成功率仅为42.2%，而TeamHOI达到97.5%，差距高达55.3个百分点。这一鸿沟的根本原因在于：CooHOI\*-n的MLP策略架构将输入维度固定为特定团队规模，无法动态适应队友数量的变化；同时，其隐式依赖物体共享动态进行通信，缺乏对队友状态的显式感知，导致大规模团队下协调失效。

**重载条件下的表现**更为悬殊。当桌面重量提升至5倍时，CooHOI\*-8的成功率骤降至4.1%，几乎完全失效；而TeamHOI仍保持81.1%的成功率（提升+77.0个百分点）。这表明Transformer架构中的交叉注意力机制能够有效整合任意数量队友的状态信息，使策略在极端物理条件下仍能维持分布式协作。

定性可视化（Figure 4）进一步印证了这一结论：TeamHOI在4智能体和8智能体配置下均展现出同步且稳定的团队行为，桌面运动轨迹平滑；而CooHOI\*基线在8智能体场景中表现出明显的不协调和低效协作。

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison across 4-agent (top) and 8-agent (bottom) configurations. Our method produces synchronized and stable teamwork across both cases, whereas the CooHOI* baselines exhibit limited or ineffective cooperation. Red line indicates the table’s movement trajectory, and the black dot marks its final position at the end of each episode*

### 消融实验：关键组件的因果验证

#### 掩码AMP策略

掩码AMP是解决协作行为多样性瓶颈的核心机制。传统全身AMP（Full-body AMP）要求策略模仿单人参考运动中的全身动作，但在物体交互期间，手部与物体的接触模式在单人数据和多人协作场景之间存在本质差异——强行模仿会抑制策略探索多样化的手-物交互行为。

消融实验（Figure 5）证实：移除掩码AMP后，举升阶段的成功率显著下降，且手-物交互行为变得单一。掩码AMP通过在交互期间掩码与物体接触的身体部位（如手部），释放了这些部位的探索自由度，同时保持非接触部位（如腿部）的动作自然性。其混合风格奖励公式为：

$$r_{t}^{\mathrm{style}} = \sigma(\alpha_{t}) r_{t}^{\mathrm{mask}} + (1-\sigma(\alpha_{t})) r_{t}^{\mathrm{full}}$$

其中 $\sigma(\alpha_t)$ 根据交互程度动态调节全身与掩码鉴别器奖励的权重，实现了从自然行走到接触交互的平滑过渡。

#### 队形奖励

队形奖励由角度分散奖励 $r_{\mathrm{ang}}$ 和主轴覆盖奖励 $r_{\mathrm{cov}}$ 加权组合而成：

$$r_{\mathrm{form}} = 0.25 r_{\mathrm{ang}} + 0.75 r_{\mathrm{cov}}$$

角度分散奖励鼓励智能体围绕桌面中心均匀分布，避免拥挤在一侧导致力矩失衡。主轴覆盖奖励（Figure 3）则衡量智能体支撑多边形沿物体两个主轴方向的覆盖程度，引导队形沿桌面长轴对齐——这种配置能提供最稳定的支撑，有利于自然行走。

消融对比（Figure 6）显示：仅使用角度分散奖励时，智能体虽能均匀分布但队形方向随机，行走姿态不自然；加入主轴覆盖奖励后，智能体自发形成沿桌面主轴对齐的稳定队形，行走动作更加流畅。这验证了 $r_{\mathrm{cov}}$ 在将分布式接触点转化为结构化支撑队形中的关键作用。

### 零样本泛化能力

Table 4展示了统一策略在未见过的桌面尺寸（小型和大型）上的零样本泛化性能。策略无需任何微调即可适应不同几何形状的物体，成功率的下降幅度有限，表明Transformer架构学到的协调策略具有几何无关的特性。定性可视化（Figure 9）显示，智能体能够根据桌面尺寸自动调整站位间距和队形布局。

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/014_Figure_9.jpg]]
*Figure 9: Qualitative visualization of the zero-shot generalization under unseen table geometries and team sizes. Red line indicates the table’s movement trajectory, and the black dot marks its final position at the end of each episode*

### 失败模式与局限性

尽管TeamHOI在2至8智能体范围内表现优异，但在极大规模团队（如16个智能体）下，合作时间比例降至约15.1%。这表明当空间拥挤程度超过一定阈值时，基于局部观测的分布式策略难以有效协调所有智能体——部分智能体可能因无法接近桌面而成为“旁观者”。

掩码AMP的另一潜在风险在于：被掩码身体部位的运动完全依赖任务奖励引导。当任务奖励设计不当时（例如举升奖励权重不足），可能导致被掩码部位产生不自然的动作。这要求任务奖励函数的设计需与掩码策略紧密配合。

此外，当前方法仅在桌子搬运这一单一任务上验证，虚拟智能体使用简化的球状手部模型（无手指），限制了精细操作能力。方法向更复杂的多人物交互任务（如合作运动、舞蹈）的推广仍需进一步研究。

![[assets/figures/papers/paper_list_l1755_TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interacti/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison across team sizes (2A, 4A, 8A). Our method achieves consistently high success rates, collective cooperation, and motion smoothness across all settings using a single unified policy. Unlike CooHOI* baselines, where agent formations are pre-defined, our agents must infer cooperation to establish stable formations autonomously, making the coordination requirement more demanding. Under the heavy-load setting (5× table weights), only our method demonstrates effective cooperation among eight agents. All results are averaged over 10,000 simulation episodes*

## 定位与知识库关联

### 1. 方法沿革与基线定位

TeamHOI 解决的核心瓶颈是物理仿真中多智能体协作的两个刚性约束：**固定团队规模** 与 **协作行为多样性不足**。此前方法在这两条轴线上存在明确的能力边界。

**CooHOI 及其改进基线** 构成了最直接的对比参照系。原版 CooHOI 采用基于 MLP 的策略架构，输入维度固定，因此每个策略只能服务于预定义的智能体数量；同时，其协作机制隐式依赖物体共享动态进行通信，未显式感知队友状态。为公平比较，作者对 CooHOI 进行了大幅增强——融入掩码 AMP 与接触点导向奖励，形成 **CooHOI\*-n** 基线（n=2,4,8，独立训练）。即便如此，该基线仍受限于预定义接触点与缺乏队友令牌，在 8 智能体场景下成功率仅 42.2%，重载（5× 桌面重量）时更骤降至 4.1%（Table 1）。这直接验证了 MLP 架构的规模泛化瓶颈。

**AMP 系列方法** 构成了动作先验维度的谱系背景。标准全身 AMP 通过鉴别器鼓励策略生成与参考运动分布一致的姿态过渡，但在多智能体协作场景中面临两难：若严格要求全身动作与单人参考运动对齐，则手-物交互行为被过度约束；若放宽约束，则非交互身体部位的动作自然性下降。TeamHOI 的掩码 AMP 策略在交互期间掩码与物体接触的身体部位，仅对非接触部位施加风格监督，从而在保持整体动作自然性的同时释放了手部行为的多样性空间。这一设计本质上是对 AMP 框架在“部分约束”场景下的条件化扩展。

**Transformer 策略架构** 的选择直接对标了近年来将序列建模引入强化学习的趋势。与 MLP 策略不同，Transformer 的自注意力与交叉注意力机制天然支持可变长度输入，使得策略可以处理任意数量的队友令牌。这一架构选择并非孤立创新，而是将 NLP 和 CV 领域已验证的集合建模能力迁移至多智能体协调问题，其关键适配在于将队友状态编码为令牌并作为交叉注意力的键值对。

### 2. 方法谱系中的结构性贡献

从知识库定位角度看，TeamHOI 的贡献可分解为三个可独立评估的“槽位替换”：

| 槽位 | 基线值 | TeamHOI 替换 | 证据锚点 |
|------|--------|-------------|---------|
| 策略网络架构 | 固定尺寸 MLP，无显式队友通信 | Transformer + 队友令牌交叉注意力 | Section 3.2, Figure 2 |
| 动作先验 | 标准全身 AMP | 掩码 AMP（按交互程度混合全身/掩码鉴别器） | Section 3.2, Equation (4), Figure 5 |
| 队形协调 | 预定义手部接触点，无队形奖励 | 角度分散 + 主轴覆盖队形奖励，不依赖团队数量与形状 | Section 3.3.1, Equations (5)-(7), Figure 3, Figure 6 |

这三个槽位之间存在因果耦合：Transformer 架构提供了处理可变规模队友的容量，掩码 AMP 提供了从单人参考运动扩展协作行为的自由度，主轴覆盖奖励则为分布式协调提供了不依赖预定义接触点的引导信号。消融实验分别验证了掩码 AMP 对举升阶段成功率的提升（Figure 5）以及主轴覆盖奖励对沿物体主轴对齐队形的塑造作用（Figure 6）。

### 3. 适用边界与局限

**已验证的适用边界**：
- 任务类型：合作搬运（桌子），含重载变体（5× 重量）
- 团队规模：2 至 8 个智能体，单一统一策略覆盖
- 物体几何：训练用标准桌面，零样本泛化至小尺寸和大尺寸桌面（Table 4）
- 行为多样性：通过调整任务奖励可扩展至侧持、边缘抬举等多可供性行为（Figure 10）

**明确局限**：
- **极大规模团队退化**：在 16 个智能体场景下，合作时间比例仅约 15.1%，表明拥挤环境中的队形协调仍存在瓶颈。这暗示当前基于局部观测的分布式策略在密集场景中可能缺乏足够的全局协调信息。
- **掩码 AMP 的任务奖励依赖性**：掩码身体部位的动作由任务奖励引导，当任务奖励设计不当时可能损害动作自然性。这意味着该方法对奖励工程的敏感度较高。
- **训练效率**：多阶段训练总耗时约 9.5 天，且依赖精心设计的课程学习，限制了快速迭代和任务迁移的可行性。
- **任务泛化未验证**：仅在桌子搬运任务上进行了系统评估，未展示在合作运动、舞蹈、战斗等其他协作 HOI 任务上的表现。
- **手部建模简化**：虚拟智能体使用简化的球状手部，无手指关节，可能限制精细操作任务的直接迁移。

### 4. 开放问题

1. **任务谱系扩展**：如何将统一策略框架迁移至更复杂的多人物交互任务（如合作运动、双人舞蹈、对抗性战斗）？这些任务对时序同步性和角色分工的要求可能超出当前奖励设计的表达能力。

2. **参考运动数据的利用效率**：当前掩码 AMP 仅使用单人参考运动。若能引入少量多人协作参考运动数据，是否可进一步提升动作多样性和自然性，同时降低对任务奖励的依赖？

3. **Sim-to-Real 的通信挑战**：在真实多机器人系统中，感知延迟和通信不可靠性是常态。当前假设的完美观测共享在实际部署中难以满足，如何设计鲁棒的延迟感知策略是一个关键工程问题。

4. **队形奖励的通用性**：主轴覆盖奖励依赖于物体的主轴定义，对于不规则形状物体或非对称协作任务（如仅在一侧施力），需要设计更通用的支撑质量度量。

5. **动态角色分配**：当前策略中所有智能体执行同质化行为。能否引入角色分工机制（如领航员-跟随者），通过层级化协调优化大规模团队的协作效率？这可能需要结合图神经网络或分层强化学习框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/TeamHOI_Learning_a_Unified_Policy_for_Cooperative_Human_Object_Interactions_with_Any_Team_Size.pdf]]
