---
title: "HY-Motion 1.0: Scaling Flow Matching Models for Text-To-Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation.pdf
project_link: null
code_link: https://github.com/Tencent-Hunyuan/HY-Motion-1.0
aliases:
- HM10
- HM10SFMMTMG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将基于DiT的流匹配模型参数规模提升至十亿级（1B），配合3000小时大规模预训练和强化学习（DPO/Flow-GRPO）对齐，是打破瓶颈的关键干预点。
primary_logic: 大规模预训练赋予模型广泛的运动语义先验，高质量微调提升动作精度，而强化学习弥合统计似然与人类偏好的鸿沟——这是实现高可控性、高逼真度文本到动作生成的可扩展路径。
claims:
- HY-Motion 1.0在所有6大动作类别的指令遵循平均得分上显著超越DART、LoM、GoToZero和MoMask等基线。
- HY-Motion 1.0在动作质量平均得分上同样取得最高分，所有类别均领先。
- 模型规模从0.46B扩展到1B时，指令遵循能力持续提升（3.20 → 3.34），而动作质量在0.46B后接近饱和。
- 仅用400小时数据训练的DiT-0.46B-400h指令遵循得分（3.05）远低于使用3000小时预训练的DiT-0.46B（3.20），证明数据量对指令遵循的关键作用。
---

# HY-Motion 1.0: Scaling Flow Matching Models for Text-To-Motion Generation

> [!tip] 核心洞察
> 大规模预训练赋予模型广泛的运动语义先验，高质量微调提升动作精度，而强化学习弥合统计似然与人类偏好的鸿沟——这是实现高可控性、高逼真度文本到动作生成的可扩展路径。

| 字段 | 内容 |
|------|------|
| 中文题名 | HY-Motion 1.0：将流匹配模型扩展到十亿参数用于文本到动作生成 |
| 英文题名 | HY-Motion 1.0: Scaling Flow Matching Models for Text-To-Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/Tencent-Hunyuan/HY-Motion-1.0) · [paper](https://arxiv.org/abs/2512.23464) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HY-Motion 1.0 |
| Dataset | 指令遵循能力（6大类别人类评估） |

> [!tip] 效果简介
> - 指令遵循能力（6大类别人类评估） 上，平均分数 (1-5) 3.24（最高） vs 其他最佳方法得分显著更低 (N/A)。
> - 动作质量（6大类别人类评估） 上，平均分数 (1-5) 3.43（最高） vs 其他最佳方法得分显著更低 (N/A)。
> - 指令遵循缩放实验（模型尺寸） 上，平均分数 DiT-1B: 3.34 vs DiT-0.46B: 3.20 (+0.14)。

## 概要

### 问题与瓶颈

文本驱动的人体动作生成近年来取得了显著进展，但现有方法普遍受限于模型容量不足、训练数据规模与质量有限，导致两大核心问题：**指令遵循能力差**——模型难以精确捕捉文本描述中的细粒度语义约束；**动作伪影频发**——生成结果常出现脚滑、漂浮、物理不自然等现象。这些瓶颈的根源在于，当前主流模型多采用小规模扩散或自回归架构，训练数据局限于HumanML3D等公开数据集，缺乏对广泛运动语义的充分建模。

### 核心思路

HY-Motion 1.0 提出了一条可扩展的解决路径：**将基于DiT的流匹配模型参数规模提升至十亿级（1B），并配合三阶段训练范式**，从数据、容量与对齐三个维度系统性地突破上述瓶颈。具体而言：

- **大规模预训练**：在超过3000小时的清洗后运动数据上进行预训练，赋予模型广泛的运动语义先验，这是提升指令遵循能力的关键。
- **高质量微调**：在近400小时精心整理的数据上进行微调，提升动作精度与细节表现。
- **强化学习对齐**：引入DPO与Flow-GRPO，弥合统计似然与人类偏好之间的鸿沟，进一步强化物理合理性与指令一致性。

该方法的核心洞察在于：模型容量的扩展与数据规模的扩大并非简单的“更大即更好”，而是通过三阶段训练实现了**语义理解—动作精度—人类偏好**的递进式对齐。

### 主要结果

在涵盖6大动作类别、200+子类的人类评估中，HY-Motion 1.0 在**指令遵循能力**（Table 1，平均得分3.24）和**动作质量**（Table 2，平均得分3.43）两项指标上均显著超越DART、LoM、GoToZero、MoMask等基线方法。消融实验进一步揭示：

- **模型规模效应**：从0.46B扩展到1B，指令遵循能力持续提升（3.20 → 3.34），而动作质量在0.46B后趋于饱和（Tables 3–4）。
- **数据规模效应**：仅用400小时数据训练的DiT-0.46B-400h指令遵循得分仅为3.05，远低于使用3000小时预训练的DiT-0.46B（3.20），证明大规模多样化数据对指令遵循的关键作用（Table 3）。

### 方法定位

HY-Motion 1.0 在方法谱系中处于**大规模流匹配生成模型**与**强化学习对齐**的交叉点。相较于基于离散标记的自回归模型（如LoM, Chen et al., CVPR 2025）或掩码建模方法（如MoMask, Guo et al., CVPR 2024），HY-Motion 1.0 的核心区分点在于：首次将DiT架构的流匹配模型扩展至十亿参数，并系统性地引入RLHF阶段的偏好对齐。与同样探索大规模数据的GoToZero（Fan et al., ICCV 2025）相比，HY-Motion 1.0 的贡献更侧重于**模型容量扩展与训练范式的协同设计**，而非单纯的数据规模堆砌。

该工作的局限性包括：自动标注流水线对高度复杂指令的语义捕捉可能存在不足；未显式建模物体几何，人-物交互动作的物理准确性有待提升；在极长或不常见运动类型上的表现尚未充分验证。代码已开源（https://github.com/Tencent-Hunyuan/HY-Motion-1.0）。

### 问题背景

文本到动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的3D人体运动序列，在游戏动画、虚拟人驱动、影视制作等领域具有广阔的应用前景。近年来，扩散模型和自回归模型在该任务上取得了显著进展，但现有方法普遍受限于两个关键瓶颈：

1. **模型容量不足**：当前主流方法多采用小规模扩散或自回归架构，参数量有限，难以充分捕获文本与运动之间的复杂映射关系，导致指令遵循能力薄弱——模型往往无法准确执行描述中的所有语义要素。
2. **数据规模与质量受限**：现有工作大多依赖HumanML3D等公开数据集，其数据量仅数十小时，且动作类别覆盖范围窄、标注粒度粗。这进一步加剧了模型对长尾动作和复合指令的泛化困难，并导致脚滑（foot sliding）、根节点漂移（root drift）等物理不自然的动作伪影频繁出现。

这些瓶颈共同造成了一个根本性困境：**统计似然与人类偏好之间存在鸿沟**——即使模型在训练数据上实现了低损失，生成的样本仍可能在语义准确性、物理合理性和运动自然度上偏离人类预期。

### 现有方法缺口

当前文本到动作生成领域的方法可大致归为以下几类，但各自存在明显局限：

- **扩散自回归模型**（如 **DART**，Zhao et al., ICLR 2025）：将扩散过程与自回归生成结合，但模型规模有限，难以覆盖多样化动作空间。
- **基于LLM的离散标记模型**（如 **LoM**，Chen et al., CVPR 2025）：利用语言模型的序列建模能力处理离散运动标记，但离散化本身可能损失运动细节的连续性。
- **零样本生成方法**（如 **GoToZero**，Fan et al., ICCV 2025）：尝试在百万级数据上实现零样本泛化，但缺乏对特定指令的精细对齐机制。
- **掩码建模方法**（如 **MoMask**，Guo et al., CVPR 2024）：通过掩码重建学习运动先验，但在复杂语义理解和长序列生成上表现不足。

上述方法的共同缺陷在于：**均未系统性地探索模型与数据的规模化扩展**，也未引入强化学习来弥合似然最大化与人类偏好之间的鸿沟。这为更大容量模型、更大规模数据和偏好对齐训练留下了明确的改进空间。

### 本文动机

针对上述瓶颈，HY-Motion 1.0 的核心动机在于验证一条可扩展的技术路径：**通过规模化扩展模型容量、训练数据量和引入强化学习对齐，能否系统性地提升文本到动作生成的指令遵循能力和动作质量？**

具体而言，本文做出以下关键干预：

- **架构规模化**：首次将基于DiT（Diffusion Transformer）的流匹配模型参数规模提升至十亿级（1B），突破现有方法的容量天花板。
- **三阶段训练范式**：构建大规模预训练（3000小时）→ 高质量微调（400小时）→ 强化学习对齐（DPO + Flow-GRPO）的完整训练管线，分别解决语义先验获取、动作精度提升和人类偏好对齐三个层次的问题。
- **偏好对齐创新**：引入直接偏好优化（DPO）和针对流匹配模型定制的组相对策略优化（Flow-GRPO），通过语义奖励与物理惩罚的联合优化，直接弥合统计似然与人类偏好的鸿沟。

这一动机背后的核心洞察是：**大规模预训练赋予模型广泛的运动语义先验，高质量微调提升动作精度，而强化学习则是实现高可控性、高逼真度文本到动作生成的关键闭环**。

## 核心方法与创新机理

HY-Motion 1.0 的核心创新可归结为三个关键维度的系统性升级：**模型容量**、**训练范式**与**数据规模/质量**。这些维度并非孤立改进，而是相互耦合——大规模数据为十亿参数模型提供足够的语义先验，而强化学习对齐则在统计似然之上叠加人类偏好约束，最终实现指令遵循能力与动作逼真度的双重突破。

### 1. 架构变革：从中小规模模型到十亿参数流匹配 DiT

现有文本驱动动作生成模型（如 **DART** (Zhao et al., ICLR 2025)、**LoM** (Chen et al., CVPR 2025)、**MoMask** (Guo et al., CVPR 2024)）普遍采用中小规模扩散或自回归架构，模型容量受限，难以充分捕获复杂运动语义与物理约束。HY-Motion 1.0 首次将基于 DiT 的流匹配模型成功扩展到十亿参数（1B）级别（*Section 1*），这一容量跃升使模型能够学习更丰富、更细粒度的运动-文本联合分布。

具体而言，HY-Motion DiT 采用混合 Transformer 架构，融合双流与单流处理模块，对运动序列与文本条件进行联合建模（*Section 3.2*）。运动序列被表示为 $N$ 帧的集合 $\pmb x = \{ \pmb f_1, \pmb f_2, \dots, \pmb f_N \}$，每帧 $\pmb f \in \mathbb{R}^{201}$ 包含全局根位移、全局身体朝向、局部关节旋转及局部关节位置（*Section 3.1*）。训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1} [ || \mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t) - \mathbf{v}_t ||_2^2 ]$$

推理时通过积分预测速度场生成运动：$d\mathbf{x} / dt = \mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t)$（*Section 3.2*）。

### 2. 训练范式跃迁：三阶段渐进式训练

传统方法多采用单阶段或两阶段训练，难以同时兼顾语义广度与动作精度。HY-Motion 1.0 提出三阶段训练框架（*Section 1*）：

- **阶段一：大规模预训练**。在 3000+ 小时清洗后的多样化运动数据上训练，赋予模型广泛的运动语义先验。
- **阶段二：高质量微调**。将训练源切换至精心整理的约 400 小时高质量数据集 $\mathcal{D}_{\mathrm{HQ}}$，学习率衰减至预训练阶段的 0.1 倍（$\eta_{\mathrm{ft}} = 0.1 \times \eta_{\mathrm{pre}}$），提升动作精度与细节表现。
- **阶段三：强化学习对齐**。弥合统计似然与人类偏好的鸿沟，是该框架的关键差异化环节。

第三阶段包含两种互补的偏好对齐策略：

**直接偏好优化（DPO）** 直接从人类偏好数据中引导策略，其损失函数为：

$$\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}; \pi_{\mathrm{ref}}) = - \mathbb{E}_{(c, x_w, x_l) \sim \mathcal{D}_{\mathrm{pref}}} \left[ \log \sigma \left( \beta \log \frac{\pi_{\theta}(x_w|c)}{\pi_{\mathrm{ref}}(x_w|c)} - \beta \log \frac{\pi_{\theta}(x_l|c)}{\pi_{\mathrm{ref}}(x_l|c)} \right) \right]$$

该损失最大化胜者样本 $x_w$ 与败者样本 $x_l$ 在策略概率比上的差距（*Section 4.3*）。

**Flow-GRPO** 是专为流匹配模型定制的组相对策略优化变体，其单步目标为：

$$f(r, \hat{A}, \theta, \epsilon, \beta) = \frac{1}{G} \sum_{i=1}^{G} \frac{1}{T} \sum_{t=1}^{T} \Big( \min \big( r_t^i(\theta) \hat{A}^i, \mathrm{clip}(r_t^i(\theta), 1-\epsilon, 1+\epsilon) \hat{A}^i \big) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Big)$$

其中 $r_t^i(\theta) = \frac{p_{\theta}(\mathbf{x}_{t-1}^i | \mathbf{x}_t^i, \mathbf{c})}{p_{\mathrm{ref}}(\mathbf{x}_{t-1}^i | \mathbf{x}_t^i, \mathbf{c})}$ 为当前策略与参考策略在时间步 $t$ 的概率比（*Section 4.3*）。奖励函数整合了语义奖励（由自定义训练的 Text-Motion Retrieval 模型评估）与物理奖励（对脚滑、根漂移等伪影施加硬惩罚），从而在强化学习阶段显式约束物理合理性。

### 3. 数据工程：规模与质量的双重突破

数据是支撑模型容量扩展的隐性创新。现有方法多依赖有限公开数据集（如 HumanML3D），而 HY-Motion 1.0 构建了包含采集、处理、过滤、标注四步的数据整理流水线（*Section 2, Figure 2*）。所有运动数据通过重定向、低质量过滤与规范化三步标准化至统一的 SMPL-H 骨架（*Section 2.1*），并建立六级粗粒度到 200+ 细粒度的层次化动作类别体系（*Section 2.2, Figure 3*）。最终形成 3000+ 小时预训练数据与近 400 小时高质量微调数据的组合，为模型提供了前所未有的语义覆盖与动作多样性。

### 创新点的因果关联

这三项创新构成一条因果链：**大规模数据**是十亿参数模型有效训练的基石，消融实验表明同样 0.46B 模型在仅 400 小时数据上训练时指令遵循得分下降 0.15（*Table 3*）；**模型容量扩展**（0.46B → 1B）持续提升指令遵循能力（3.20 → 3.34），但动作质量在 0.46B 后趋于饱和（*Tables 3-4*）；**强化学习对齐**则在统计似然基础上进一步注入人类偏好与物理约束，弥补容量扩展无法解决的伪影问题。三者协同，使 HY-Motion 1.0 在所有六大动作类别的指令遵循（平均 3.24）与动作质量（平均 3.43）人类评估中均显著超越 DART、LoM、GoToZero、MoMask 等基线（*Tables 1-2*）。

HY-Motion 1.0 构建了一条三阶段训练流水线，将文本到动作生成从有限容量的扩散/自回归模型推向十亿参数级的流匹配范式。其核心瓶颈在于：现有模型受限于小规模架构和低质量训练数据，导致指令遵循能力弱，并频繁出现脚滑、物理不自然等动作伪影。HY-Motion 1.0 通过“大规模预训练—高质量微调—强化学习对齐”的递进式干预，系统性地打破了这一瓶颈。

### 流水线总览

整个框架（Figure 4）由四个功能模块串联而成，形成从文本输入到 3D 动作输出的端到端流：

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the HY-Motion 1.0 framework*

1. **时长预测与提示重写 LLM**  
   接收用户自由文本，预测目标动作的合理帧数，并将用户提示重写为结构化、细粒度的动作描述，作为后续模块的条件输入。

2. **双编码器文本条件提取**  
   采用 **Qwen3-8B** 提取逐词嵌入，结合 **CLIP-L** 提取全局语义嵌入，二者共同构成条件信号 $\mathbf{c}$，注入生成模型。

3. **HY-Motion DiT（核心生成引擎）**  
   基于 DiT 架构的流匹配扩散 Transformer，参数规模可扩展至 1B。它接收噪声初始状态 $\mathbf{x}_T$ 和文本条件 $\mathbf{c}$，通过预测速度场 $\mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t)$ 并沿 ODE 路径积分生成运动序列。该模块采用混合 Transformer 设计，融合双流与单流处理块，以联合建模运动与文本的分布。

4. **强化学习对齐模块（第三阶段）**  
   在预训练和微调之后，引入 **DPO** 和 **Flow-GRPO** 进行偏好对齐。奖励函数整合语义奖励（由自定义 Text-Motion Retrieval 模型评估）和物理奖励（对脚滑、根漂移等施加硬惩罚），弥合统计似然与人类偏好之间的鸿沟。

### 数据流与训练阶段

三阶段训练范式是框架的关键干预点，每个阶段对应不同的数据规模与优化目标：

- **阶段一：大规模预训练**  
  使用超过 3000 小时的清洗后多样化运动数据，以恒定学习率 $\eta_{\text{pre}}$ 优化条件流匹配损失：
  $$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1} \left[ \| \mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t) - \mathbf{v}_t \|_2^2 \right]$$
  此阶段赋予模型广泛的运动语义先验，是后续指令遵循能力的基础。

- **阶段二：高质量微调**  
  切换至精心整理的约 400 小时高质量数据集 $\mathcal{D}_{\text{HQ}}$，学习率衰减至 $\eta_{\text{ft}} = 0.1 \times \eta_{\text{pre}}$。此阶段提升动作精度与细节表现。

- **阶段三：强化学习对齐**  
  首先使用 DPO 直接从人类偏好对中引导策略：
  $$\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}; \pi_{\mathrm{ref}}) = -\mathbb{E}_{(c, x_w, x_l) \sim \mathcal{D}_{\mathrm{pref}}} \left[ \log \sigma \left( \beta \log \frac{\pi_{\theta}(x_w|c)}{\pi_{\mathrm{ref}}(x_w|c)} - \beta \log \frac{\pi_{\theta}(x_l|c)}{\pi_{\mathrm{ref}}(x_l|c)} \right) \right]$$
  随后采用 Flow-GRPO，在时间步级别施加裁剪优势目标与 KL 惩罚，强化物理合理性。

### 输入输出规格

- **输入**：自由文本描述（如“一个人向前走，同时挥动右手”）。
- **中间表示**：运动序列表示为 $N$ 帧的集合 $\mathbf{x} = \{\mathbf{f}_1, \mathbf{f}_2, \dots, \mathbf{f}_N\}$，每帧 $\mathbf{f} \in \mathbb{R}^{201}$，包含全局根位移（3 维）、全局身体朝向（6 维）、局部关节旋转和局部关节位置。
- **输出**：统一 SMPL-H 骨架的 3D 人体运动序列，可重定向至不同角色（Figure 1 底部示例）。

### 关键设计决策

消融实验（Tables 3–4）揭示了两个决定性机制：**数据量是指令遵循的瓶颈**——仅用 400 小时训练的 DiT-0.46B 指令遵循得分（3.05）远低于使用 3000 小时预训练的同等模型（3.20）；**模型规模对指令遵循的增益持续到 1B**（3.20 → 3.34），而动作质量在 0.46B 后趋于饱和。这验证了“大规模预训练赋予语义先验，强化学习弥合偏好鸿沟”的核心洞察。

### 运动序列表示

HY-Motion 1.0 将一段人体运动序列形式化为 $N$ 帧的集合，每帧编码为一个 201 维的向量：

$$ \pmb x = \{ \pmb f_1, \pmb f_2, \dots, \pmb f_N \}, \quad f \in \mathbb{R}^{201} $$

该 201 维向量由四部分拼接而成：全局根位移（$\mathbb{R}^3$）、全局身体朝向（$\mathbb{R}^6$）、局部关节旋转（$\mathbb{R}^{132}$）和局部关节位置（$\mathbb{R}^{60}$）。这一表示同时保留了运动学链的层次结构与末端效应器的空间位置，为后续流匹配建模提供了信息完备的连续表征。

### 条件流匹配损失函数

HY-Motion DiT 采用条件流匹配（Conditional Flow Matching）作为核心训练目标。给定噪声样本 $\mathbf{x}_0$、目标运动 $\mathbf{x}_1$ 和文本条件 $\mathbf{c}$，模型 $\mathbf{v}_\theta$ 在时间 $t$ 预测速度场，并与真实速度 $\mathbf{v}_t$ 计算 L2 损失：

$$ \mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1} \left[ \| \mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t) - \mathbf{v}_t \|_2^2 \right] $$

其中 $\mathbf{x}_t$ 由线性插值路径 $\mathbf{x}_t = t\mathbf{x}_1 + (1-t)\mathbf{x}_0$ 构造，真实速度 $\mathbf{v}_t = \mathbf{x}_1 - \mathbf{x}_0$。这一目标直接回归速度场，避免了扩散模型中噪声预测的间接性，在推理时可通过求解常微分方程生成运动：

$$ d\mathbf{x} / dt = \mathbf{v}_\theta(\mathbf{x}_t, \mathbf{c}, t) $$

### 直接偏好优化损失（DPO）

在第三阶段强化学习对齐中，HY-Motion 1.0 引入 DPO 将人类偏好直接注入策略模型。给定文本条件 $c$、胜者样本 $x_w$ 和败者样本 $x_l$，DPO 损失最大化胜者相对败者的对数概率比：

$$ \mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}; \pi_{\mathrm{ref}}) = - \mathbb{E}_{(c, x_w, x_l) \sim \mathcal{D}_{\mathrm{pref}}} \left[ \log \sigma \left( \beta \log \frac{\pi_{\theta}(x_w|c)}{\pi_{\mathrm{ref}}(x_w|c)} - \beta \log \frac{\pi_{\theta}(x_l|c)}{\pi_{\mathrm{ref}}(x_l|c)} \right) \right] $$

其中 $\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为冻结的参考策略（第二阶段微调后的模型），$\beta$ 控制偏离参考策略的惩罚强度，$\sigma$ 为 sigmoid 函数。该损失无需显式奖励模型，直接从成对偏好数据中学习。

### Flow-GRPO 策略优化目标

为进一步强化物理合理性并弥补 DPO 在严格边界约束上的不足，HY-Motion 1.0 采用 Flow-GRPO——一种针对流匹配模型的组相对策略优化变体。整体目标在时间步上取平均：

$$ \mathcal{L}_{\mathrm{Flow-GRPO}}(\pi_{\theta}; \pi_{\mathrm{ref}}) = \mathbb{E}_{c \sim \mathcal{D}_{\mathrm{GRPO}}, \{x^i\}_{i=1}^{G} \sim \pi_{\mathrm{ref}}(\cdot|c)} \left[ f(r, \hat{A}, \theta, \epsilon, \beta) \right] $$

其中 $G$ 为每组采样数，单步目标 $f$ 定义为：

$$ f(r, \hat{A}, \theta, \epsilon, \beta) = \frac{1}{G} \sum_{i=1}^{G} \frac{1}{T} \sum_{t=1}^{T} \Big( \min \big( r_t^i(\theta) \hat{A}^i, \mathrm{clip}(r_t^i(\theta), 1-\epsilon, 1+\epsilon) \hat{A}^i \big) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Big) $$

核心在于每个时间步 $t$ 的策略概率比：

$$ r_t^i(\theta) = \frac{p_{\theta}(\mathbf{x}_{t-1}^i | \mathbf{x}_t^i, \mathbf{c})}{p_{\mathrm{ref}}(\mathbf{x}_{t-1}^i | \mathbf{x}_t^i, \mathbf{c})} $$

其中 $\hat{A}^i$ 为组内标准化后的优势值，$\epsilon$ 为裁剪阈值，KL 散度项约束策略更新幅度。该目标将流匹配的逐步去噪过程显式纳入策略优化，使奖励信号（语义奖励 $R_{\mathrm{sem}}$ 与物理惩罚 $R_{\mathrm{phy}}$）能够沿生成轨迹反向传导，从而直接抑制脚滑、根漂移等物理伪影。

### 关键模块协同

上述公式对应 HY-Motion 1.0 三阶段训练框架的核心计算单元：**流匹配损失**驱动大规模预训练建立运动语义先验，**DPO 损失**在高质量微调后实现偏好对齐，**Flow-GRPO 目标**则通过显式物理奖励弥合统计似然与人类偏好的剩余鸿沟。三者逐层递进，共同支撑从十亿参数 DiT 到高可控性动作生成的完整路径。

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/005_Figure_5.jpg]]
*Figure 5: Model architecture of our HY-Motion DiT*

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the data processing pipeline*

## 实验与关键发现

HY-Motion 1.0 的实验评估围绕两个核心维度展开：**指令遵循能力**（模型是否准确执行文本描述的动作语义）和**动作质量**（生成动作是否物理合理、无脚滑等伪影）。评估采用人类主观评分（1-5分），覆盖6大粗粒度动作类别及其下属200+细粒度子类：Locomotion、Sports & Athletics、Fitness & Outdoor Activities、Daily Activities、Social Interactions & Leisure、Game Character Actions。

### 与SOTA方法的对比

在指令遵循能力上，HY-Motion 1.0 在所有6个动作类别上均取得最高分，平均得分3.24，显著超越 **DART**（Zhao et al., ICLR 2025）、**LoM**（Chen et al., CVPR 2025）、**GoToZero**（Fan et al., ICCV 2025）和 **MoMask**（Guo et al., CVPR 2024）等基线方法（Table 1）。在动作质量维度，HY-Motion 1.0 同样全面领先，平均得分3.43（Table 2）。这一双维度优势表明，大规模流匹配模型不仅在语义对齐上更强，同时生成的3D人体运动更加自然、物理合理。

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/006_Table_1.jpg]]
*Table 1: Instruction-following capability comparison with state-of-the-art text-to-motion models. Motion categories: (a) Locomotion, (b) Sports & Athletics, (c) Fitness & Outdoor Activities, (d) Daily Activities, (e) Social Interactions & Leisure, and (f) Game Character Actions*

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/007_Table_2.jpg]]
*Table 2: Motion quality comparison with state-of-the-art text-to-motion models. Motion categories: (a) Locomotion, (b) Sports & Athletics, (c) Fitness & Outdoor Activities, (d) Daily Activities, (e) Social Interactions & Leisure, and (f) Game Character Actions*

### 缩放效应分析：模型规模与数据量

Tables 3-4 揭示了模型规模和数据量对性能的差异化影响：

- **指令遵循能力随模型规模持续提升**：从 DiT-0.46B（3.20）到 DiT-1B（3.34），增幅为+0.14。这表明更大的模型容量能更好地编码复杂的文本-运动映射关系。
- **动作质量在0.46B后接近饱和**：DiT-0.46B 的动作质量平均得分已达3.26，DiT-1B 仅小幅提升至3.34。这说明物理合理性等低层运动属性对模型容量的需求较低，中等规模已能较好捕捉。
- **预训练数据量是指令遵循的关键瓶颈**：DiT-0.46B-400h（仅用400小时高质量数据训练，无预训练）的指令遵循得分仅为3.05，相比使用3000小时预训练的 DiT-0.46B（3.20）下降了0.15。这一消融直接证明了大规模多样化预训练数据对于建立广泛运动语义先验的不可替代性。

### 失败模式与局限性

尽管整体性能优异，分析中仍识别出以下不足：

1. **复杂指令的语义捕捉不完美**：自动标注流水线在处理高度细致或复杂的动作指令时可能产生偏差，导致模型对极端语义的理解不够精准。
2. **人-物交互的物理准确性不足**：由于未显式建模物体几何信息，涉及人与物体交互的动作（如拿起特定形状的工具）可能出现物理不自然的接触或穿透。
3. **长序列与罕见动作的泛化未充分验证**：模型在极长时间跨度或不常见运动类型上的表现尚缺乏系统评估，实际部署中需注意这些场景的退化风险。

### 关键图表结论

- **Table 1 & Table 2**：HY-Motion 1.0 在指令遵循和动作质量两个维度上全面超越现有SOTA方法，确立了新的性能标杆。
- **Tables 3-4**：模型规模的缩放收益在指令遵循上更显著，而动作质量在中等规模后趋于饱和；大规模预训练数据是指令遵循能力的决定性因素。
- **Figure 1（定性对比）**：可视化结果直观展示了HY-Motion 1.0 在动作多样性和语义一致性上相比基线的优势，同时验证了模型对不同角色骨架的泛化能力。

![[assets/figures/papers/paper_list_l88_HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation/figures/008_Table_3.jpg]]
*Table 3: Instruction-following capability comparison of different model sizes. Motion categories: (a) Locomotion, (b) Sports & Athletics, (c) Fitness & Outdoor Activities, (d) Daily Activities, (e) Social Interactions & Leisure, and (f) Game Character Actions. The model “DiT-0.46B-400h” is trained only on the 400-hour high-quality dataset, while the other models are pretrained on the 3,000-hour dataset*

## 定位与知识库关联

### 基线关系与差异化

HY-Motion 1.0 在文本到动作生成领域与以下代表性基线方法形成对比：

- **DART**（Zhao et al., ICLR 2025）：扩散自回归运动生成模型。HY-Motion 1.0 在指令遵循和动作质量上均显著超越，其核心差异在于用流匹配替代自回归范式，并将模型规模推至十亿参数级。
- **LoM**（Chen et al., CVPR 2025）：基于 LLM 和离散运动标记的生成模型。HY-Motion 1.0 采用连续流匹配而非离散标记，避免了量化信息损失，同时通过大规模预训练获得更丰富的运动先验。
- **GoToZero**（Fan et al., ICCV 2025）：百万级数据的零样本文本到动作生成。HY-Motion 1.0 在数据规模上提升了一个数量级（3000+小时 vs. 百万级数据），并引入强化学习对齐，弥补了统计似然与人类偏好的鸿沟。
- **MoMask**（Guo et al., CVPR 2024）：基于掩码建模的 3D 人体动作生成。HY-Motion 1.0 的 DiT 流匹配架构在生成质量和指令遵循上均表现出显著优势。

从方法谱系看，HY-Motion 1.0 属于**大规模流匹配生成模型**这一新兴分支，其关键差异化在于三阶段训练范式——大规模预训练（3000小时）+ 高质量微调（400小时）+ 强化学习对齐（DPO + Flow-GRPO）——而非仅依赖单一阶段或两阶段训练。这一范式使模型在指令遵循能力上获得决定性增益：消融实验表明，同样 0.46B 模型，仅用 400 小时数据训练时指令遵循得分下降 0.15（3.20 → 3.05），验证了大规模预训练的关键作用。

### 适用边界

- **数据覆盖范围**：模型在 6 大类 200+ 小类动作上进行了评估，涵盖 Locomotion、Sports & Athletics、Fitness & Outdoor Activities、Daily Activities、Social Interactions & Leisure 和 Game Character Actions。在这些类别内模型表现优异，但极长或不常见运动类型上的表现尚未充分验证。
- **骨架结构**：所有数据统一到 SMPL-H 骨架，模型未验证对其他骨架结构（如非人形骨架、手部精细骨架）的泛化能力。
- **物理建模深度**：强化学习阶段引入的物理奖励（惩罚脚滑、根漂移等伪影）在一定程度上缓解了物理不合理问题，但未显式建模物体几何，人与物体交互动作的物理准确性可能不足。

### 局限与开放问题

**已识别的局限**：

1. **自动标注流水线的语义上限**：自动标注流水线可能无法完美捕捉高度复杂或细致的指令语义，这限制了模型在极端精细指令下的表现天花板。
2. **人-物交互的物理准确性**：未显式建模物体几何，导致涉及外部物体的动作（如持物、推拉）可能缺乏物理合理性。该问题需要手动验证具体交互场景的生成质量。
3. **分布外泛化未充分验证**：在极长序列或不常见运动类型上的表现缺乏系统评估。

**开放问题**：

1. **标注流水线的改进方向**：如何改进标注流水线以处理高度细致或复杂的动作指令？这直接关系到模型指令遵循能力上限的进一步提升。
2. **人-物交互的隐式建模**：如何在不显式提供物体几何的条件下生成物理准确的人-物交互动作？可能的路径包括从大规模数据中隐式学习交互约束，或引入物理仿真作为训练信号。
3. **三阶段训练范式的泛化性**：该训练范式（大规模预训练 + 高质量微调 + RL 对齐）能否泛化到其他骨架结构或动作生成任务（如面部动作、手势生成）？这决定了方法谱系的扩展潜力。
4. **模型规模与动作质量的饱和现象**：消融实验显示动作质量在 0.46B 后接近饱和（3.26 → 3.34），而指令遵循能力持续提升（3.20 → 3.34）。这表明单纯增大模型规模对动作质量的边际收益递减，未来可能需要新的架构设计或训练目标来突破这一瓶颈。

## 原文 PDF

![[paperPDFs/arxiv_2025/HY_Motion_1_0_Scaling_Flow_Matching_Models_for_Text_To_Motion_Generation.pdf]]
