---
title: "Duolando: Follower GPT with Off-Policy Reinforcement Learning for Dance Accompaniment"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_Accompaniment.pdf
project_link: https://lisiyao21.github.io/projects/Duolando
code_link: https://github.com/karpathy/minGPT
aliases:
- Duolando
tags:
- ICLR_2024
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入离线策略强化学习（off-policy RL）微调GPT，利用人工定义的步级奖励（特别是基于下肢速度与相对位移偏差的惩罚）来对齐跟随者的下肢运动与全局位移，从而消除滑步并增强对分布外（OOD）条件的鲁棒性。
primary_logic: 将舞蹈伴奏建模为基于GPT的自回归序列生成任务，使用预训练的VQ-VAE对动作与相对位移进行量化；在此基础上，离线RL赋予模型在没有真实标签的情况下，依据人为定义的奖励探索可行动作路径的能力，有效解决OOD场景下的滑步问题并提升交互质量。
claims:
- 完整Duolando相比无RL变体，滑步比(SR)从1.06%降至0.33%，下降69%。
- 引入RL后，FID_k从106.72降至25.30（改善76%），同时交互指标显著提升（FID_cd从21.68降至9.97）。
- 离线RL使用显式概率目标（Eq.5），避免了在线AC方法中因负优势值持续压低旧样本概率的缺陷。
- 单独去除前瞻机制（LAT）导致FID_k上升26.01（20%下降），证明前瞻信息对运动流畅性至关重要。
---

# Duolando: Follower GPT with Off-Policy Reinforcement Learning for Dance Accompaniment

> [!tip] 核心洞察
> 将舞蹈伴奏建模为基于GPT的自回归序列生成任务，使用预训练的VQ-VAE对动作与相对位移进行量化；在此基础上，离线RL赋予模型在没有真实标签的情况下，依据人为定义的奖励探索可行动作路径的能力，有效解决OOD场景下的滑步问题并提升交互质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Duolando：基于离线策略强化学习的舞蹈伴奏跟随者GPT |
| 英文题名 | Duolando: Follower GPT with Off-Policy Reinforcement Learning for Dance Accompaniment |
| 会议/期刊 | ICLR 2024 |
| Links | [Project](https://lisiyao21.github.io/projects/Duolando) · [Code](https://github.com/karpathy/minGPT) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Duolando |
| Dataset | DD100 |

> [!tip] 效果简介
> - DD100 (test set) 上，FID_k (↓) - 跟随者运动质量 25.30 vs 78.52 (Bailando) (-53.22 (68% improvement))；FID_k (↓) - 跟随者运动质量 25.30 vs 69.14 (EDGE) (-43.84 (63% improvement))；FID_cd (↓) - 交互协调质量 9.97 vs 21.68 (Duolando w/o RL) (-11.71 (54% reduction))。

## 概要

**核心问题**：舞蹈伴奏任务要求生成与领舞者实时协调的跟随者动作。现有GPT或独舞方法在此任务中面临两个关键瓶颈——下肢运动与全局位移不一致导致的**滑步伪影**，以及在未见过的音乐/领舞条件下**稳定性差**、难以保持协调交互。

**核心方法**：本文提出 **Duolando**，将舞蹈伴奏建模为基于GPT的自回归序列生成任务。其核心创新在于引入**离线策略强化学习（off-policy RL）** 微调GPT，利用人工定义的步级奖励（特别是基于下肢速度与相对位移偏差的惩罚）来对齐跟随者的下肢运动与全局位移，从而消除滑步并增强对分布外（OOD）条件的鲁棒性。

**关键结论**：
- 完整Duolando相比无RL变体，**滑步比（SR）从1.06%降至0.33%，下降69%**（Table 6），证明离线RL有效对齐下肢运动与全局位移。
- 引入RL后，跟随者运动质量指标 **FID_k 从106.72降至25.30（改善76%）**，交互协调指标 **FID_cd 从21.68降至9.97**（Table 2），在运动质量与交互协调性上均取得显著提升。
- 离线RL使用显式概率目标（Eq.5），避免了在线Actor-Critic方法中因负优势值持续压低旧样本概率的缺陷。

**方法定位**：Duolando属于**两阶段舞蹈生成框架**——第一阶段使用VQ-VAE将身体部位动作与相对位移量化为离散码本序列；第二阶段基于交互协调GPT自回归预测跟随者token，并通过离线RL微调以适配OOD场景。相比独舞基线（如 **Bailando**（Siyao et al., 2022）、**EDGE**（Tseng et al., 2023）），Duolando首次将领舞者条件与离线RL结合，显式建模双人交互。

**局限提示**：用户研究中完整Duolando仅在约15%的对比中超过真实舞蹈，生成质量与专业舞者仍有较大差距；离线RL的奖励设计主要针对滑步问题，未显式考虑接触质量、风格保持等更细粒度的交互维度。



### 双人舞蹈伴奏：从独舞生成到交互协调

音乐驱动的舞蹈生成近年来取得显著进展，然而主流工作——如 **Bailando**（Siyao et al., 2022）和 **EDGE**（Tseng et al., 2023）——几乎全部聚焦于**独舞**场景：模型仅以音乐为条件，生成单个舞者的动作序列。当任务扩展到**双人舞蹈伴奏**（dance accompaniment）时，系统需要同时感知音乐节奏与领舞者（leader）的动作，并生成跟随者（follower）与之协调互动。这一转变引入了独舞方法无法解决的三个核心挑战：

1. **交互协调（Interaction Coordination）**：跟随者动作必须在空间和时间上与领舞者保持有意义的关联，包括接触帧（contact frames）的匹配和节奏一致性。独舞基线缺乏领舞条件输入，其交互指标极差——例如，Duolando 的消融实验显示，去掉交互协调模块后接触帧比例（CF）仅为 7.04%，而完整模型可达 52.36%（Table 2）。

2. **下肢运动与全局位移的一致性**：标准 GPT 或现有独舞方法在生成跟随者动作时，容易出现**滑步伪影**（skating artifacts）——即下肢关节运动幅度很小，但角色在空间中产生显著位移。这一现象源于模型未能对齐局部关节速度与全局位移导数。在 Duolando 的消融中，仅监督训练的变体滑步比（SR）高达 1.06%（Table 6）。

3. **分布外（OOD）条件的鲁棒性**：测试时遇到的音乐-领舞组合可能显著偏离训练分布。纯监督模型在面对 OOD 条件时缺乏探索能力，生成的动作容易崩溃为不协调或物理上不可行的序列。

### 现有方法的瓶颈

现有舞蹈生成方法可归纳为两条技术路线：

- **独舞生成模型**（如 Bailando、EDGE）：通常基于 VQ-VAE 量化动作 + GPT/扩散模型自回归生成。它们能够生成高质量的单人舞蹈，但完全忽略了交互维度，无法直接迁移至伴奏任务。
- **双人交互运动生成**：早期工作多依赖运动图（motion graph）或检索匹配，缺乏对未见条件的泛化能力；基于学习的方法则受限于数据规模和交互建模的显式设计。

**根本瓶颈**在于：监督训练范式使模型仅学会模仿训练分布内的模式，当面对 OOD 条件时，模型缺乏一个**探索可行解空间**的机制，导致滑步、交互失败等问题集中暴露。

### 本文动机与核心思路

Duolando 的提出旨在系统性解决上述瓶颈。其核心洞察是：将舞蹈伴奏建模为基于 GPT 的自回归序列生成任务，并引入**离线策略强化学习（off-policy RL）**作为微调手段。这一设计的关键因果逻辑在于：

- **VQ-VAE 量化**：将身体部位动作和跟随者-领舞者相对位移压缩为离散 token，使 GPT 能够以统一的自回归方式处理多模态条件。
- **交互协调 GPT**：通过 10×10 块状下三角注意力掩码，同时处理音乐、领舞动作和跟随者历史，保持因果顺序的同时实现多序列融合。
- **离线 RL 微调**：利用人工定义的步级奖励（特别是基于下肢速度与相对位移偏差的惩罚，见 Eq. 6），赋予模型在无真实标签的情况下探索可行动作路径的能力。**离线 RL 的显式概率目标（Eq. 5）避免了在线 Actor-Critic 方法中因负优势值持续压低旧样本概率的缺陷**，使模型能够有效复用历史数据，在 OOD 条件下稳定生成无滑步的协调动作。

这一动机在实验中得到有力验证：引入离线 RL 后，滑步比从 1.06% 降至 0.33%（下降 69%，Table 6），交互质量指标 FID_cd 从 21.68 降至 9.97（改善 54%，Table 2），同时运动质量 FID_k 从 106.72 降至 25.30（改善 76%）。这些结果表明，**监督预训练提供生成基础，离线 RL 赋予 OOD 鲁棒性与物理一致性**，二者互补构成了解决舞蹈伴奏任务的有效范式。



## 核心方法与创新机理

Duolando 的核心创新在于将**舞蹈伴奏（dance accompaniment）重新建模为基于 GPT 的自回归序列生成任务**，并通过**离线策略强化学习（off-policy RL）** 赋予模型在分布外（OOD）条件下自我纠错的能力。与现有独舞生成方法（如 Bailando、EDGE）仅以音乐为条件不同，Duolando 同时接收音乐与领舞者（leader）动作作为条件，自回归地预测跟随者（follower）的全身运动序列及两者的相对位移。

### 关键创新槽位

#### 1. GPT 微调策略：从纯监督到离线 RL

- **基线**：标准 GPT 仅通过交叉熵损失进行监督训练（supervised training，ST），依赖训练集中的真实标签序列。
- **提出方案**：在监督预训练后，引入**离线策略强化学习**（off-policy RL）进行微调。核心损失函数为：

$$ \mathcal{L}_{RL}^{\mathrm{off}}(\theta) = \sum_{t=0}^{T-1} -\log(1 - \operatorname{abs}[\pi_{\theta}(\hat{a}_t|\hat{s}_t) - \sigma(Q(\hat{s}_t, \hat{a}_t))]) $$

该损失通过单调映射 $\sigma$ 将策略概率 $\pi_\theta$ 与 Q 值对齐，允许模型**复用历史生成数据**进行训练，无需在线采样。相比在线 Actor-Critic 方法（Eq.4），离线 RL 避免了因负优势值持续压低旧样本概率而导致的训练不稳定问题（Section 3.3）。

**因果机制**：在 OOD 条件下（如未见过的音乐或领舞动作），监督训练的 GPT 缺乏真实标签引导，容易产生下肢运动与全局位移不一致的**滑步伪影（skating artifacts）**。离线 RL 通过人为定义的步级奖励（Eq.6）——当预测位移导数与下肢速度的偏差 $\delta$ 超过阈值时施加惩罚 $-\eta \cdot \delta$——直接优化生成策略，使模型学会在无标签情况下自主探索可行动作路径。实验表明，引入 RL 后滑步比（SR）从 1.06% 降至 0.33%，下降 69%（Table 6）。

#### 2. 相对位移预测：从无监督解码到显式 VQ-VAE 建模

- **基线**：通过无监督速度解码分支间接推断跟随者的全局位移。
- **提出方案**：构建独立的**相对位移 VQ-VAE**（$VQ^{tr}$），将跟随者与领舞者的相对位移量化为离散 token，直接作为 GPT 的输出预测目标之一（Section 3.1, Figure 3b）。

**因果机制**：显式建模相对位移使 GPT 能够直接学习空间协调关系。消融实验证实，单独添加相对位移预测（tr）使交互协调指标 FID_cd 从 4803 骤降至 21.68（Table 2），但同时也引入了滑步问题（SR 升至 1.06%）。这一矛盾恰好由 RL 解决——RL 的下肢奖励直接约束位移与腿部运动的一致性，实现了**交互质量与运动物理合理性的双重提升**。

#### 3. 交互协调注意力掩码：从标准因果注意力到块状下三角矩阵

- **基线**：标准因果自注意力或未明确交互掩码。
- **提出方案**：采用 **10×10 块状下三角矩阵**作为注意力掩码（Section 3.2）。该掩码同时处理 10 个输入序列（音乐、领舞者四部分肢体 token、跟随者四部分肢体 token、相对位移 token），在保持因果顺序的同时实现跨序列的信息融合。

**因果机制**：块状下三角结构确保了自回归生成的因果性（未来 token 不可见当前 token），同时允许跟随者的当前生成步充分关注领舞者的历史运动与音乐节奏，是实现双人协调交互的基础架构支撑。

#### 4. 前瞻机制：从当前帧条件到未来 L 帧信息利用

- **基线**：仅使用当前帧的条件信息。
- **提出方案**：通过**前瞻 Transformer（Look-Ahead Transformers, LAT）** 将未来 $L$ 帧的音乐与领舞动作信号传播到当前步（Section 3.2, Section B.2）。具体而言，在采样条件输入时额外提取 $L$ 个未来 token，通过波段注意力掩码注入 GPT。

**因果机制**：前瞻信息使模型能够“预见”即将到来的音乐节拍与领舞动作变化，从而生成更流畅、更具预判性的跟随动作。消融实验表明，去除前瞻机制导致运动质量指标 FID_k 上升 26.01（约 20% 退化），但对交互指标影响小于 7%（Table 5），说明前瞻主要作用于单肢运动流畅性而非跨角色协调。

### 创新点之间的协同关系

上述四个创新槽位并非孤立存在，而是形成了一条完整的因果链：

1. **显式相对位移预测** 赋予了模型空间协调的能力，但引入了滑步副作用；
2. **离线 RL 与步级奖励** 专门针对滑步问题进行纠偏，同时提升 OOD 鲁棒性；
3. **交互协调注意力掩码** 提供了多序列融合的架构基础；
4. **前瞻机制** 进一步提升了运动的时间连贯性。

这一设计使得 Duolando 在交互质量（FID_cd 从 21.68 降至 9.97）、运动质量（FID_k 从 106.72 降至 25.30）和物理合理性（SR 降至 0.33%）三个维度上均实现了显著提升（Table 2, Table 6）。



Duolando采用两阶段流水线架构，将舞蹈伴奏任务建模为基于GPT的自回归序列生成问题。第一阶段通过VQ-VAE对运动与空间关系进行离散化编码，第二阶段由交互协调GPT在量化空间中自回归生成跟随者动作序列，并引入离线策略强化学习（off-policy RL）微调以消除滑步伪影并提升分布外（OOD）鲁棒性。

**第一阶段：运动量化编码。** 系统使用四个独立的Motion VQ-VAE分别对跟随者与领舞者的四个身体部位（上半身、下半身、左手、右手）进行编码与量化，将连续3D关节序列映射为离散code序列 $z^{up}, z^{down}, z^{lhand}, z^{rhand}$。同时，一个额外的相对位移VQ-VAE（Relative Translation VQ-VAE）对跟随者与领舞者之间的相对位移 $tr$ 进行量化编码，为后续GPT提供空间交互的离散表示。VQ-VAE的训练损失由关节位置与旋转矩阵的重建损失、码本损失和承诺损失组成（Eq.1）。

**第二阶段：交互协调GPT自回归生成。** GPT以10路输入并行处理音乐特征 $m$、领舞者的四个部位量化序列 $z^{up\oplus}, z^{down\oplus}, z^{lhand\oplus}, z^{rhand\oplus}$ 以及跟随者历史序列，通过10×10块状下三角注意力掩码（block-wise lower-triangular mask）保持因果顺序，自回归预测跟随者下一时间步的五个输出token——四个身体部位的运动码 $z^{up\odot}, z^{down\odot}, z^{lhand\odot}, z^{rhand\odot}$ 和相对位移码 $z^{tr}$。为增强长期连贯性，前瞻机制（Look-Ahead Transformers, LAT）在每一步将未来 $L$ 帧的条件信号通过波段注意力掩码传播至当前步，使模型在生成时感知未来的音乐与领舞动作信息。

**第三阶段：离线RL微调。** 在监督预训练完成后，GPT进入离线RL微调阶段（Figure 5b）。与依赖在线采样的Actor-Critic方法不同，Duolando使用离线RL损失（Eq.5）直接对齐策略概率与Q值，允许复用历史生成数据。奖励函数以步级下肢奖励 $r_t^{down}$（Eq.6）为核心：当预测位移导数与下肢速度的偏差 $\delta$ 低于阈值时给予正奖励，否则施加比例惩罚 $-\eta \cdot \delta$，从而强制对齐下肢运动与全局位移，消除滑步伪影。

**数据流总结：** 音乐与领舞动作（条件信号）→ LAT前瞻嵌入 → 交互协调GPT（10路因果注意力）→ 自回归输出跟随者运动码与相对位移码 → VQ-VAE解码器重建3D关节序列与全局位置。RL阶段在GPT自生成的OOD样本上计算步级奖励，通过离线RL损失反向优化网络权重。

### 补充图表

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/005_Figure_4.jpg]]
*Figure 4: Structure of follower GPT. The GPT takes ten inputs and autoregressively predicts the subsequent tokens of follower’s motion and the relative translation. Preconditions (music signals and leader’s motion) are integrated with Look-Ahead Transformers (LAT)*



Duolando采用两阶段流水线：先通过VQ-VAE将连续运动序列离散化为code序列，再由交互协调GPT自回归地生成跟随者动作。以下按模块顺序解析关键公式与设计。

### 3.1 运动量化：VQ-VAE

**模块角色**：将高维连续运动（3D关节旋转与位置）压缩为离散token，为GPT提供可建模的符号空间。系统共使用五个VQ-VAE：四个分别处理上半身、下半身、左手、右手的运动，一个独立处理跟随者与领舞者的相对位移。

**训练损失**（Eq.1）：

$$\mathcal{L}_{VQ} = \mathcal{L}_{rec}(\hat{p}, p) + \mathcal{L}_{rec}(\hat{M}, M) + \| \mathrm{sg}(f) - z \| + \lambda \| f - \mathrm{sg}(z) \|$$

其中：
- $\mathcal{L}_{rec}(\hat{p}, p)$：关节位置的重建损失
- $\mathcal{L}_{rec}(\hat{M}, M)$：旋转矩阵的重建损失
- $\| \mathrm{sg}(f) - z \|$：码本损失，将编码器输出 $f$ 与最近码本向量 $z$ 对齐（$\mathrm{sg}$ 为stop-gradient操作）
- $\lambda \| f - \mathrm{sg}(z) \|$：承诺损失，约束编码器输出不要偏离码本向量过远，$\lambda$ 为权重系数

量化过程为 $z_k = \arg\min_{z \in \mathcal{Z}} \| f_i - z \|$，即从码本 $\mathcal{Z}$ 中选择与编码特征 $f_i$ 最接近的向量作为离散表示。

### 3.2 交互协调GPT与前瞻机制

**模块角色**：以自回归方式，在音乐和领舞者动作的条件下，生成跟随者的量化动作序列与相对位移。

**最大似然目标**（Eq.2）：

$$(z^{up\odot}, z^{down\odot}, z^{lhand\odot}, z^{rhand\odot}, z^{tr}) = \operatorname*{argmax} \operatorname{Pr}(z \mid m, z^{up\oplus}, z^{down\oplus}, z^{lhand\oplus}, z^{rhand\oplus})$$

其中：
- $z^{up\odot}, z^{down\odot}, z^{lhand\odot}, z^{rhand\odot}$：跟随者上半身、下半身、左手、右手的量化动作token序列
- $z^{tr}$：相对位移的量化token序列
- $m$：音乐特征条件
- $z^{\cdot\oplus}$：领舞者对应身体部位的量化动作token序列

**交互协调注意力掩码**：GPT的输入为10个序列（音乐+领舞4部位+跟随者4部位+相对位移），使用 $10 \times 10$ 的块状下三角注意力掩码，确保每个序列在自回归生成时只能关注自身及先前时间步的信息，同时保持各序列间的因果顺序。

**前瞻机制（Look-Ahead Transformers, LAT）**：在前向推断时，GPT不仅接收当前时间步的条件信号，还额外提取未来 $L$ 帧的条件信息（音乐与领舞者动作），通过波段注意力掩码将未来条件传播到当前步的预测中（Eq.3）：

$$z_{1,\dots,T}^{\dots} = \mathrm{GPT}(\widetilde{m}_{0,\dots,T-1}, \widetilde{z}_{0,\dots,T-1}^{\dots}, z_{0,\dots,T-1}^{\dots})$$

其中 $\widetilde{m}$ 和 $\widetilde{z}$ 为截断的前瞻嵌入，$z$ 为历史跟随者编码。该机制使模型在生成当前帧时能“预见”即将到来的音乐节拍和领舞动作，从而提升运动流畅性与长期连贯性。

### 3.3 离线策略强化学习微调

**模块角色**：在监督训练完成后，使用离线RL微调GPT，使其在分布外（OOD）条件下也能根据人工奖励生成合理动作，核心解决滑步问题。

**问题背景**：在线Actor-Critic方法（Eq.4）在更新时使用当前策略采样的动作计算优势 $A$：

$$\mathcal{L}_{AC}^{\mathrm{on}}(\theta) = \sum_{t=0}^{T-1} -\log(\pi_{\theta}(\hat{a}_t^{\theta} \mid \hat{s}_t^{\theta})) \cdot A$$

当优势值 $A$ 为负时，该损失会压低旧样本（来自历史策略）的概率，导致无法有效复用离线数据。

**离线RL损失（本方法核心，Eq.5）**：

$$\mathcal{L}_{RL}^{\mathrm{off}}(\theta) = \sum_{t=0}^{T-1} -\log(1 - \operatorname{abs}[\pi_{\theta}(\hat{a}_t \mid \hat{s}_t) - \sigma(Q(\hat{s}_t, \hat{a}_t))])$$

其中：
- $\pi_{\theta}(\hat{a}_t \mid \hat{s}_t)$：当前策略网络对动作 $\hat{a}_t$ 的预测概率
- $Q(\hat{s}_t, \hat{a}_t)$：状态-动作对的Q值估计
- $\sigma(\cdot)$：单调映射函数，将Q值映射到 $[0,1]$ 区间
- $\operatorname{abs}[\cdot]$：取绝对值

该损失通过最小化策略概率与Q值映射之间的绝对偏差，使策略输出与Q值对齐，而非简单地按优势方向缩放。由于不依赖当前策略的采样动作，可直接在历史生成样本上训练，实现对离线数据的复用。

**下肢步级奖励（Eq.6）**：

$$r_t^{down} = \begin{cases} 1, & \text{if } \delta < \text{threshold}, \\ -\eta \cdot \delta, & \text{otherwise} \end{cases}$$

其中：
- $\delta$：预测相对位移的时间导数与下肢关节速度之间的偏差
- $\text{threshold}$：偏差阈值（实验中设为0.03）
- $\eta$：惩罚系数（实验中设为100）

该奖励直接对齐下肢运动与全局位移：当二者一致（偏差小）时给予正奖励，否则施加与偏差成比例的惩罚，从而引导模型消除滑步伪影。

**监督训练到RL的转换桥梁**（Eq.8）：监督学习的交叉熵损失可重写为RL中动作对数概率的形式：

$$\mathcal{L}_{ST}(\theta) = \sum_{t=0}^{T-1} -\log(\pi_{\theta}(a_t \mid s_t))$$

这为从监督预训练平滑过渡到RL微调提供了统一的优化框架。

### 补充图表

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/004_Figure_3.jpg]]
*Figure 3: (a) Structures of Motion VQ-VAEs and (b) Relative Translation VQ-VAE. The quantization is to substitute a encoded feature to the most similar one*



## 实验与关键发现

### 核心瓶颈与因果机制

Duolando 要解决的核心瓶颈在于：标准 GPT 或现有独舞方法在生成跟随者动作时，容易出现下肢运动与全局位移不一致的**滑步伪影**（skating artifacts），且在未见过的音乐/领舞条件下稳定性差，难以保持协调的交互。其因果调节旋钮是通过**离线策略强化学习**（off-policy RL）微调 GPT，利用人工定义的步级奖励（特别是基于下肢速度与相对位移偏差的惩罚）来对齐跟随者的下肢运动与全局位移，从而消除滑步并增强对分布外（OOD）条件的鲁棒性。

核心洞察在于：将舞蹈伴奏建模为基于 GPT 的自回归序列生成任务，使用预训练的 VQ-VAE 对动作与相对位移进行量化；在此基础上，离线 RL 赋予模型在没有真实标签的情况下，依据人为定义的奖励探索可行动作路径的能力，有效解决 OOD 场景下的滑步问题并提升交互质量。

### 主实验结果

在 DD100 测试集上，完整 Duolando 在跟随者运动质量指标 **FID_k** 上达到 **25.30**，相比独舞基线 **Bailando**（Siyao et al., 2022）的 78.52 降低 53.22（68% 改善），相比 **EDGE**（Tseng et al., 2023）的 69.14 降低 43.84（63% 改善）。在交互协调质量指标 **FID_cd** 上，Duolando 达到 **9.97**，相比无 RL 变体（Duolando w/o RL）的 21.68 降低 11.71（54% 改善）。接触帧比例 **CF** 达到 **52.36%**，而移除交互协调的消融变体（w/o RL tr IC）仅 7.04%，提升 7.4 倍。

滑步比 **SR** 从无 RL 变体的 1.06% 降至完整 Duolando 的 **0.33%**，下降 69%（Table 6），直接验证了 RL 对齐下肢运动与全局位移的有效性。节奏对齐指标 **BED** 达到 0.2858，音乐对齐指标 **BAS** 为 0.2046，均显著优于独舞基线。

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/012_Table_6.jpg]]
*Table 6: Skating ratio (SR) of different methods. The SR is calculated as the percentage of the number of frames with negligible leg movement but significant global displacement*

需要注意的是，独舞基线（Bailando, EDGE）未考虑领舞条件，其交互指标（如 FID_cd, CF）因缺乏交互信息而极差，比较时需注意任务设定差异。Ground Truth 的 FID_k 为 6.56，FID_cd 为 3.41，CF 为 74.25%，表明生成质量与真实舞蹈仍有较大差距。

### 消融实验

**离线 RL 的核心作用**：引入离线 RL 后，FID_k 从 106.72 降至 25.30（改善 76%），FID_cd 从 21.68 降至 9.97，SR 从 1.06% 降至 0.33%。这证明 RL 不仅解决了滑步问题，还显著提升了运动质量和交互协调性。单独添加相对位移预测（tr）大幅改善交互指标（FID_cd 从 4803 降至 21.68），但引入了滑步问题（SR 升至 1.06%），RL 有效解决了这一矛盾（Table 2, Table 6）。

**前瞻机制（LAT）的影响**：去除前瞻机制导致 FID_k 从 25.30 升至 51.31（20% 退化），但交互指标变化小于 7%（Table 5），证明前瞻信息对运动流畅性至关重要，但对交互协调的影响相对有限。

**音乐输入的影响**：随机化音乐输入使 BAS 略微提升 1.3%，但 BED 下降 10%（Table 4），表明音乐对节奏对齐有重要影响，但对运动多样性的影响相对较小。

### 方法谱系与知识库定位

Duolando 在舞蹈生成领域的方法谱系中，位于独舞生成基线（Bailando, EDGE）的延伸位置。与仅以音乐为条件的独舞方法不同，Duolando 同时融合音乐、领舞动作和跟随者历史，通过交互协调注意力掩码实现双人舞蹈伴奏。其关键创新在于将离线 RL 引入 GPT 的微调阶段，区别于纯监督训练方法。离线 RL 使用显式概率目标（Eq.5），避免了在线 AC 方法中因负优势值持续压低旧样本概率的缺陷。

### 失败模式与局限性

尽管 Duolando 在定量指标上表现优异，但用户研究中完整模型仅在约 15% 的对比中超过真实舞蹈，整体生成质量与专业舞者仍有较大差距。离线 RL 的奖励设计主要针对滑步问题（下肢速度与位移一致性），未显式考虑接触质量、美学等更细粒度的交互维度，可能导致生成动作在视觉自然度上仍有不足。DD100 数据集规模有限（约 117 分钟，10 种风格），可能限制模型对极端 OOD 条件的泛化能力。

### 重要图表结论

**Table 2** 展示了完整定量基准，Duolando 在所有交互指标（FID_cd, CF）上均取得最优，在运动质量指标（FID_k）上显著超越独舞基线。**Table 6** 直接量化了 RL 对滑步问题的消除效果（SR 从 1.06% 降至 0.33%）。**Table 5** 揭示了前瞻机制对运动流畅性的关键作用。**Table 4** 验证了音乐输入对节奏对齐的重要性。

### 补充图表

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/007_Table_2.jpg]]
*Table 2: Quantitative benchmark for dance accompaniment. The first place and runner-up are highlighted in bold and underlined, respectively. S denotes a solo dance generation model that does not take the leader into condition, while D denotes that one does. *Since solo dance has no interaction, the cross-distance between two agents are completely irregular, making the diversity particularly high*

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/011_Table_5.jpg]]
*Table 5: Ablation study on looking ahead (LA)*

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/010_Table_4.jpg]]
*Table 4: Ablation studies for music input. represents random music input*

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/003_Table_1.jpg]]
*Table 1: Comparison with human-human interaction and music-to-dance datasets. HHI denotes Human-Human Interaction, where S represents Strong interaction with physical contact while W means Weak interaction== like repeated motion in group dance. ˇ “ ˇ “ indicates whether having accompanied music modality. « denotes whether having hand (finger-level) motions. # Subj. denotes the number of performers. T denotes average duration and T is the total duration of all sequences. MV stands for capturing with multi-view cameras. Genres for human-human interaction dataset means the type of interactions, while it indicates the music and dance styles for music-to-dance datasts. n/a means that the exact informatio...*

![[assets/figures/papers/paper_list_l1897_Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_A/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results (a) and user study (b). In qualitative results, conditioning leader is colored in gray while generated followers are in red. In boxplot of user study, triangles and colored lines are mean and median values, respectively. Circles are outliers beyond 1.5× interquartile range (3σ in normal dist.)*



## 定位与知识库关联

### 1 任务定位：从独舞生成到双人交互伴奏

Duolando 解决的是**舞蹈伴奏（dance accompaniment）**任务：给定音乐与领舞者（leader）的动作序列，自回归生成跟随者（follower）的3D舞蹈动作。这一任务与已有的**独舞生成（solo dance generation）**存在根本差异——后者仅以音乐为条件，不建模人际交互。独舞基线如 **Bailando**（Siyao et al., 2022）和 **EDGE**（Tseng et al., 2023）在DD100测试集上的交互协调指标极差（例如 Bailando 的 FID_cd 高达 4803.74，接触帧比例 CF 仅 0.58%），直接验证了独舞模型无法迁移到双人场景。

在双人交互运动生成领域，DD100数据集（Table 1）是首个同时包含强交互（物理接触）与弱交互（群舞重复动作）的音乐-舞蹈配对数据集，覆盖10种舞蹈风格。此前的人-人交互数据集（如NTU RGB+D、ShakeFive2）缺乏音乐条件，而音乐-舞蹈数据集（如AIST++、DanceRevolution）仅包含独舞。Duolando 填补了这一空白。

### 2 方法谱系：VQ-VAE + GPT + 离线RL的三阶段架构

Duolando 的方法设计可分解为三个关键技术层，每层都有明确的功能边界和消融支撑：

**层1：VQ-VAE量化编码。** 将连续动作空间离散化为code序列是GPT建模的前提。Duolando 采用四个独立的Motion VQ-VAE分别编码上半身、下半身、左手、右手的3D关节序列，外加一个Relative Translation VQ-VAE量化跟随者与领舞者的相对位移。这种分部位量化的设计（而非整体量化）使模型能够独立控制不同身体部位的生成质量。Table 2显示，单独添加相对位移预测（tr）使交互指标 FID_cd 从 4803.74 骤降至 21.68，但代价是滑步比 SR 升至 1.06%——这一矛盾正是后续RL阶段要解决的核心问题。

**层2：交互协调GPT与前瞻机制。** 自回归Transformer通过10×10块状下三角注意力掩码同时处理10个序列（音乐、领舞四部位、跟随者四部位、相对位移），在保持因果顺序的前提下实现跨序列信息融合。前瞻机制（Look-Ahead Transformers, LAT）利用波段注意力掩码将未来L帧（约4秒）的条件信号传播到当前步。Table 5消融表明，去除LAT导致 FID_k 从 25.30 升至 51.31（退化约103%），但交互指标变化小于7%，说明前瞻信息对跟随者自身运动流畅性至关重要，而对交互协调的影响相对有限。

**层3：离线策略强化学习微调。** 这是Duolando区别于纯监督GPT的关键创新。标准监督训练仅能拟合训练分布内的样本，在OOD条件（未见过的音乐/领舞组合）下性能退化严重。Duolando 引入离线RL，其核心损失函数（Eq.5）为：

$$\mathcal{L}_{RL}^{\mathrm{off}}(\theta) = \sum_{t=0}^{T-1} -\log(1 - \operatorname{abs}[\pi_{\theta}(\hat{a}_t|\hat{s}_t) - \sigma(Q(\hat{s}_t, \hat{a}_t))])$$

该损失通过单调映射 $\sigma$ 对齐策略概率与Q值，允许复用历史数据进行训练，避免了在线Actor-Critic方法中因负优势值持续压低旧样本概率的缺陷（Eq.4）。奖励函数（Eq.6）专门针对滑步问题设计：当预测位移导数与下肢速度的偏差 $\delta$ 低于阈值（0.03）时给予正奖励1，否则施加 $-\eta \cdot \delta$（$\eta=100$）的惩罚。Table 6证实，完整Duolando相比无RL变体（Duolando w/o RL），滑步比 SR 从 1.06% 降至 0.33%（下降69%），同时 FID_k 从 106.72 降至 25.30（改善76%），FID_cd 从 21.68 降至 9.97（改善54%）。

### 3 适用边界与局限

**数据规模与泛化能力。** DD100仅包含约117分钟的动作数据（10种风格），训练集约168,176帧。用户研究中完整Duolando仅在约15%的对比中超过真实舞蹈，表明生成质量与专业舞者仍有较大差距。在极端OOD条件（如训练集中未出现的舞蹈风格组合）下的泛化能力缺乏系统评估。

**奖励设计的粒度。** 当前离线RL的奖励仅针对下肢速度与位移一致性（滑步问题），未显式建模接触质量、力感传递、风格保持等更细粒度的交互维度。Table 2中接触帧比例 CF 为 52.36%，与真实舞蹈的 74.25% 仍有显著差距，说明物理接触的生成质量是当前瓶颈之一。

**计算成本。** 训练耗时约7天（4块V100 GPU），推理延迟和资源消耗未详细讨论，可能限制实时交互应用（如现场舞蹈伴奏或VR场景）。

**前瞻长度的固定性。** 前瞻长度L固定为约4秒，不同舞蹈风格或音乐速度下的最优L可能不同，当前缺乏自适应调整机制。

### 4 开放问题

1. **奖励函数的丰富化。** 能否设计更全面的奖励函数（如接触面匹配度、动作力感一致性、风格保持度）来进一步提升交互自然度？这需要更细粒度的交互标注数据。

2. **多舞伴扩展。** 当前框架基于10×10注意力掩码设计，理论上可通过扩展掩码维度支持群舞或多跟随者场景，但交互复杂度的指数增长和相对位移建模的扩展方式需要重新设计。

3. **前瞻长度的自适应。** 不同舞蹈风格（如探戈的快速步伐 vs. 华尔兹的缓慢滑动）对前瞻信息的需求可能不同，自适应调整L的机制值得探索。

4. **离线RL对预训练质量的依赖。** 离线RL的有效性是否高度依赖初始监督训练的质量？在不充分预训练的情况下，RL能否从随机策略开始学习？这一问题的答案决定了方法的鲁棒性和部署灵活性。

5. **跨领域迁移。** 本方法的VQ-VAE + GPT + 离线RL框架是否能应用于其他双人交互运动（如武术对练、体育双人项目、手语对话）？需要哪些领域特定的改动（如关节拓扑适配、交互奖励重定义）？



## 原文 PDF

![[paperPDFs/ICLR_2024/Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_Accompaniment.pdf]]
