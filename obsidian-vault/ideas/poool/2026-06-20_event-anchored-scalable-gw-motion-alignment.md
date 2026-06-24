---
title: "EASGW: 事件锚定的可扩展 MAMM / FSUGW 数据集级运动对齐"
hypothesis: |
  2026-06-21 二次复审后，本方向从“搁置”进一步标记为“作废”。根因不是实现难度，而是概念边界混淆：motion retarget 的核心对象是跨骨架/形态/拓扑的空间对应；MAMM 与 motion phase 的核心对象是动作时间结构、事件/相位/序列对齐。把 MAMM / phase / retarget 混成 dataset-level GW motion matching，会让实验验证错误问题，即使跑通也不能证明 retarget 或 phase 的核心价值。
status: invalidated
created: 2026-06-20T23:25:38+08:00
updated: 2026-06-21T17:05:00+08:00
tags:
  - motion_alignment
  - motion_matching
  - optimal_transport
  - event_anchor
  - MAMM
  - status/invalidated
source_papers:
  - "[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM]]"
  - "[[analysis/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.md|DeepPhase]]"
  - "[[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning.md|FLD]]"
  - "[[analysis/TOG_2020/LMP_Local_motion_phases_for_learning_multi_contact_character_movements.md|LMP]]"
  - "[[analysis/PACM_CGIT_2023/Motion_In_Betweening_with_Phase_Manifolds.md|Motion In-Betweening with Phase Manifolds]]"
  - "[[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog]]"
  - "[[analysis/arxiv_2025/FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Phase_Manifolds.md|FunPhase]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation.md|TransPhase]]"
  - "[[analysis/TOG_2025/Control_Operators_for_Interactive_Character_Animation.md|Control Operators]]"
web_sources:
  - "https://arxiv.org/abs/2505.19976"
  - "https://arxiv.org/abs/2308.12751"
  - "https://arxiv.org/abs/2407.18946"
  - "https://arxiv.org/abs/2512.09423"
---

# EASGW: 事件锚定的可扩展 MAMM / FSUGW 数据集级运动对齐

> [!danger] 2026-06-21 final invalidation：本方向完全作废
> 本 note 不再作为可推进 idea。核心错误是把三类对象混在一起：
>
> - **motion retarget**：主要解决骨架、形态、拓扑、局部坐标系、关节对应和 IK / 物理约束，是空间映射问题；
> - **motion phase**：主要解决周期 / 准周期运动的时间进度、节奏、过渡和局部动态同步，是时间结构问题；
> - **MAMM**：给定 source motion $X$ 与 control sequence $Y$ 后，做 pair-specific FSUGW optimization，输出 transport plan $T$ 与 aligned motion $X'$，是单样本序列对齐问题。
>
> EASGW 把 MAMM 的 pair-specific OT、phase 的动态时序信号、retarget 的跨骨架空间映射合并成“dataset-level GW motion alignment”。这会导致实验问题错位：加速 dataset-level MAMM 不能证明 retarget 能力；phase 对齐不能替代骨架对应；MAMM 在未定义共享跨骨架度量空间前也不能作为 retarget 主引擎。
>
> 替代复盘和新候选已转移到 [[ideas/poool/2026-06-21_motion-retarget-phase-mamm-boundaries.md|motion retarget / phase / MAMM 边界复盘]]。本 note 保留为失败记录，避免后续重复推进。

## 历史内容（已废弃，仅供追溯）

> [!warning] 以下内容已被上方 final invalidation 覆盖
> 后续段落记录了本方向从“可推进”到“搁置”的中间推理过程。它们不再代表当前结论，也不应作为实验方案执行。

> [!warning] 2026-06-21 update：方向搁置
> 基于对 [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM]] 技术边界和用户交互逻辑的重新审视，昨日提出的 EASGW / dataset-level MAMM 方向从“可推进”调整为 **搁置 / 待应用痛点确认**。
>
> 核心问题不是加速算法本身，而是 direction setting 不稳：MAMM 是 **pair-specific、sample-level optimization**。算法输入需要一个给定的 original motion $X$ 和一个 control sequence $Y$；论文没有提供从整个 motion database 自动选择 source motion 的机制。每次更换 $X$ 或 $Y$，transport plan $T$ 和 aligned motion $X'$ 都需要重新优化，不能复用为全局映射函数。
>
> 因此，把 MAMM 扩展成 dataset-level control-trajectory matching 目前缺少不可替代痛点。control trajectory 经过优化本身可以适配多个 source motion，作为检索 query 又不如 text description 或用户按键 / phase / motion matching 直观。即使 EASGW 加速成功，也仍然没有回答“为什么用户要用 control trajectory 从库里搜 motion”这个基础问题。
>
> **当前决策**：停止继续推进 EASGW 作为主 idea。后续若要恢复，必须先提供经审阅的具体应用场景，证明 control-trajectory / FSUGW matching 相比 text、phase、motion matching 有不可替代优势。

> [!abstract] 结论先行
> 原始想法“把 MAMM 的 FSUGW 蒸馏成 learnable / eventized phase representation”不够稳。昨日进一步收敛出的 EASGW / dataset-level acceleration 方案也被复审为应用痛点不足：它只加速 pair-specific 优化，没有解决 source motion 选择、query 交互直观性和可复用能力缺失。当前更合理的处理是：把本 note 作为已审查但搁置的方向，后续转向 FSUGW / GW 在 motion 中更明确的痛点，如可学习对齐、细粒度 text-motion 序列对齐、跨骨骼 retarget 等。

---

## 1. Idea decomposition and association

### 1.1 原始思考的拆解

来自 [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM]] 笔记中的几个问题可以拆成三条路线：

- **路线 A：learnable motion representation**  
  用 MAMM / FSUGW 的离线对齐结果作为 teacher，训练一个 motion encoder，使其输出更适合跨序列、跨控制信号对齐的 latent。
- **路线 B：dataset-level motion matching**  
  把 MAMM 从“单条 motion 与单条 control sequence 的优化器”扩展成“运动数据库上的检索、索引、批量对齐和控制轨迹检索工具”。
- **路线 C：phase 的非周期扩展**  
  周期相位对 locomotion 很强，但 kick、jump、sit、fall、pick、combat、object interaction 等事件驱动动作不一定适合用连续周期相位描述。更合理的问题是：事件、接触、速度突变和时间扭曲能否作为非周期动作的对齐锚点。

经过本地 KB、arXiv 增强检索和 DeepSeek 严肃质询后，路线 A 被降级为后续可选项，主线收敛到路线 B + C：

> **用事件/接触锚点把 FSUGW 分解成 coarse-to-fine 层次对齐，使 MAMM 从单样本优化器变成 10 万帧级 motion database alignment / retrieval 工具。**

### 1.2 为什么不主推 learnable eventized phase

DeepSeek 反驳点成立：

- “FSUGW teacher → encoder distillation”在 representation learning 上看起来像标准蒸馏，缺乏非平凡几何洞察时 ICLR 风险高。
- DeepPhase 已经声称复杂甚至非周期运动可看作多个局部周期的组合；若新方法仍叫 phase，必须证明 DeepPhase 的失败是周期归纳偏置导致，而不是通道数或训练不足。
- SIGGRAPH 更需要可见的系统价值、交互 demo 或动画生产工具；单纯 learnable latent 指标不够强。
- teacher plan 本身受 MAMM 超参数和距离缩放影响，直接蒸馏可能把脆弱性固化进 encoder。

因此本 note 明确 No-Go：**不把本阶段写成新 phase representation，不训练 encoder，不做任意拓扑 / video retarget 大系统。**

---

## 2. Real scenarios and pain points

### 2.1 真实使用场景

EASGW 面向三个实际场景：

- **Motion database retrieval / indexing**：动画师或生成系统给出一段 query motion / control trajectory，从大规模 motion library 中找结构最匹配的片段，并返回时间对齐路径。
- **Dataset-level motion matching**：对 AMASS / BABEL / HumanML3D 这类运动数据做批量对齐，构建可检索的事件段索引，为后续 inbetweening、blend、control、repair 提供候选。
- **Control trajectory retrieval**：给一条 sketch、wave、label 序列或简化事件序列，从数据库中快速找可由 MAMM 精修的 motion，而不是每个候选都跑完整 FSUGW。

### 2.2 当前方法痛点

[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM]] 的价值是 training-free、跨控制模态、只依赖域内距离结构；痛点也很明确：

- **复杂度不可扩展**：单对序列数秒到数十秒还能接受，但数据库级 all-pairs / retrieval 不可用。
- **超参数敏感**：alpha、lambda 和距离缩放影响控制服从度与运动自然度，数据库里每类动作都手工调参不可行。
- **大规模距离矩阵困难**：论文笔记已记录其不适合超过 10 万帧数据。
- **非周期动作缺少稳定粗锚点**：DeepPhase / FLD 等 phase 路线对周期或准周期运动很强，但 kick、fall、pick、combat 这类动作的关键结构更像离散事件链，而不是闭合相位环。

### 2.3 本 idea 的定位

EASGW 不试图替代 MAMM 的 FSUGW，而是把 FSUGW 变成大规模可用的局部求解器：

1. 先用事件 / 接触 / 运动学突变做粗分段；
2. 在锚点层做便宜的 coarse GW / assignment；
3. 只在候选事件段对上运行精细 FSUGW；
4. 拼接段内 transport plan，得到近似全局对齐。

---

## 3. Related-work support and research opportunities

### 3.1 Related-work overview

- [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM]]：通过 FSUGW 只比较域内距离结构，实现 sketch、wave、label、audio、motion 等任意控制序列到 motion 的 training-free 对齐。它证明了度量对齐范式可行，但没有解决 dataset-level scalability。
- [[analysis/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.md|DeepPhase]]：用 periodic autoencoder 学多通道局部相位，运动匹配对齐误差显著低于 contact-based phase 和 PCA heuristic。它证明相位流形适合运动对齐，但仍有相位通道数、技能选择、大规模异构预训练等开放问题。
- [[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning.md|FLD]]：把 PAE 扩展为显式潜在动力学，在周期 / 准周期运动上获得结构化 latent 和长期预测能力；局限是强非周期过渡可能产生较大误差。
- [[analysis/TOG_2020/LMP_Local_motion_phases_for_learning_multi_contact_character_movements.md|LMP]]：用局部接触事件为多接触动作提供局部相位，说明 contact / event 本身是有效时序锚点，但其目标是控制器学习，不是大规模 FSUGW 加速。
- [[analysis/PACM_CGIT_2023/Motion_In_Betweening_with_Phase_Manifolds.md|Motion In-Betweening with Phase Manifolds]]、[[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog]]、[[analysis/arxiv_2025/FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Phase_Manifolds.md|FunPhase]] 和 [[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation.md|TransPhase]] 说明 phase manifold 方向仍活跃；因此新工作不能泛称“phase extension”，必须切到 MAMM scalability。
- [[analysis/TOG_2025/Control_Operators_for_Interactive_Character_Animation.md|Control Operators]] 说明交互式角色动画的生产价值来自可组合控制接口和实时性；EASGW 可作为数据库检索和候选对齐底座，但本 MVP 不直接宣称完整交互系统。

### 3.2 Web-enhanced retrieval result

arXiv 增强检索的关键结果：

- 精确检索 Metric-Aligning Motion Matching 仅命中 MAMM 原论文。
- non-periodic motion phase、event phase human motion、optimal transport motion representation、dataset-level motion matching 未发现直接覆盖本切口的命中。
- Periodic Autoencoder AND motion 命中 FunPhase、Motion In-Betweening with Phase Manifolds、WalkTheDog、SMAP、Part-Wise Phase Representation 等，说明 phase autoencoder 方向仍拥挤。
- Gromov-Wasserstein AND motion alignment 命中 SyncTrack4D 一类 4DGS / multi-video 对齐工作，但不是 skeleton animation dataset-level FSUGW / MAMM 扩展。

这只能支持弱结论：**未发现直接把 MAMM / FSUGW 扩展到大规模 skeleton motion database matching 的工作**。不能写成“没人做 motion alignment / phase / OT”。

### 3.3 Research opportunity

更稳的研究空白是：

> 现有 phase 表示解决了周期/准周期对齐，MAMM 解决了单对跨域度量对齐，但还缺一个 **training-free、可扩展、事件锚定** 的框架，把 FSUGW 用于大规模运动数据库检索、对齐与控制候选筛选。

这个切口的价值来自三点：

1. **直接解决 MAMM 的已知局限**：复杂度、超参数、距离缩放和大规模数据。
2. **保留 training-free 特性**：避免 learnable representation 的 novelty 与泛化风险。
3. **事件 / 接触不是新 phase，而是加速和约束结构**：能自然覆盖非周期事件动作，也不和 DeepPhase 的 phase 表示正面争名词。

---

## 4. Frontier cross-domain techniques and validation ideas

### 4.1 方法名与核心框架

方法暂名：**EASGW，Event-Anchored Scalable Gromov-Wasserstein**。

目标：给定运动数据库 D = {M_i} 和 query 序列 Q，快速返回候选 motion 及其近似 MAMM / FSUGW 对齐计划。

核心 pipeline：

1. **事件锚点检测**  
   对每条 motion 提取锚点集合 A_i。锚点来源包括：
   - 脚 / 手 / 支撑点 contact on/off；
   - root velocity / angular velocity 的局部极值；
   - end-effector 速度过零点；
   - 高加速度 / jerk 峰值；
   - BABEL 语义片段边界或自动语义 event label（若可用）。

2. **段级 descriptor 构造**  
   每个事件段生成轻量 descriptor：
   - segment duration；
   - root displacement / turning angle；
   - contact pattern histogram；
   - mean / variance pose velocity；
   - event type logits；
   - 可选低维 pose PCA / phase descriptor。

3. **锚点级 coarse alignment**  
   在事件段 descriptor 序列上运行低成本 GW / assignment / DTW hybrid，得到候选段对应关系，而不是直接对全帧矩阵求解。

4. **段内精细 FSUGW**  
   只对被 coarse alignment 选中的短段对运行 MAMM / FSUGW。段长通常远短于完整序列，因此复杂度由 O(L^3) 降为 O(K^3 + sum_k L_k^3)，其中 K 为锚点数，L_k 为段长。

5. **transport plan 拼接与平滑**  
   将段内 T_k 拼接为全局软对齐计划 T，在段边界处加入 continuity penalty，避免 transport path 断裂。

6. **自适应距离缩放与超参选择**  
   用锚点段内统计自动选择 lambda / alpha 或距离归一化尺度：
   - 高 contact-confidence 段提高 contact 权重；
   - root path 主导段提高 trajectory 权重；
   - 高 pose variance 段降低直接 pose-distance 的主导性；
   - 若事件锚点稀疏，则回退到均匀 landmark。

### 4.2 技术贡献边界

可写贡献：

- 一个事件锚点驱动的 coarse-to-fine FSUGW 分解框架；
- 一个无需训练的自适应距离缩放 / 超参选择机制；
- 一个面向非周期事件动作的 motion database alignment benchmark；
- 若能做理论：在锚点匹配正确和段内方差有界时，近似全局 GW 误差由段内方差与锚点错配率控制。

必须删除或弱化的 claim：

- 不 claim 新 motion phase；
- 不 claim 任意拓扑 retarget；
- 不 claim 取代 MAMM；
- 不 claim learnable representation；
- 不 claim 实时交互系统，除非后续真的做 demo；
- 不 claim 跨所有非周期动作通用，先限于 clean skeleton 的 event-rich solo human motion。

### 4.3 可验证的理论 / 算法问题

最有 ICLR 味道的问题不是“跑得更快”，而是：

> 在事件锚点能近似保持跨序列语义顺序的前提下，分段 FSUGW 的解与全局 FSUGW 的误差如何受段内运动方差、锚点错配率和边界平滑项控制？

可尝试给出一个弱保证：

- 若锚点 matching 与全局最优 plan 在段级一致；
- 每个段内 pairwise distance matrix 的 Lipschitz 变化有界；
- 段边界 continuity penalty 足够强；

则 EASGW 的目标值与全局 FSUGW 最优目标之间的 gap 由段内方差、AnchorMismatchRate 和 BoundaryJump 共同控制。

这个理论不必很强，但能把论文从“工程剪枝”提升到“结构化近似”。

---

## 5. Summary and next steps

### 5.1 Focused problem statement

**最窄问题表述**：

> 如何在不训练新模型、不牺牲 MAMM 跨域度量对齐优势的前提下，将 FSUGW motion alignment 扩展到 10 万帧级运动数据库，使其支持快速 query retrieval、bulk alignment 和 control trajectory candidate search？

### 5.2 Core MVP

MVP 必须足够小，且能证伪。

**数据**：

- AMASS / BABEL clean skeleton；
- 初始规模：500 条序列，每条 3-8 秒，30 fps，总帧数约 75k；后续扩到 100k+；
- 动作类别至少覆盖：
  - 周期：walk、run；
  - 非周期事件：kick、jump、sit-down / stand-up、turn、fall / get-up、pick-up；
  - 接触丰富：stair / stumble / object-like reach。

**任务**：

1. Leave-one-out motion retrieval：每条 motion 作 query，返回数据库中最匹配序列及对齐路径。
2. Pairwise alignment approximation：抽样 motion pairs，对比 EASGW 与原始 MAMM / FSUGW 的对齐质量和速度。
3. Control trajectory candidate retrieval：用简化 sketch / event sequence 查询数据库，只做候选检索和对齐，不生成最终动画。

**Baselines**：

- MAMM / FSUGW full per-pair：质量上界；
- pose DTW；
- FastDTW；
- HMM alignment；
- DeepPhase / PAE phase + DTW；
- uniform landmark GW：去掉事件锚点的消融；
- EASGW without adaptive scaling；
- EASGW without boundary smoothing。

**指标**：

- alignment error：相对 full MAMM 的平均帧对应误差；
- event alignment error：kick impact、foot contact、sit contact、turn peak 等事件帧的时偏；
- retrieval Prec@1 / Prec@5；
- runtime per query；
- scalability：序列长度、数据库大小、总帧数增加时的 time / error 曲线；
- hyperparameter stability：不同动作类别下无需手调时的误差方差；
- failure rate：事件检测失败导致的粗匹配错配比例。

**Go / No-Go**：

- Go：
  - 平均对齐误差不超过 full MAMM 的 15%；
  - query runtime 小于 0.5 秒，或至少比 full MAMM per-candidate 快 100 倍；
  - 非周期事件动作上显著优于 DeepPhase / PAE + DTW；
  - uniform landmark 消融明显差于 event anchor，证明锚点不是普通分块。
- No-Go：
  - 事件检测不稳定，检索准确率降到 FastDTW 水平；
  - adaptive scaling 无法减少超参敏感性；
  - 与 uniform landmark GW 差距不显著；
  - 只能在 walk / run 等周期动作上有效。

### 5.3 Risks and stop-loss signals

- **事件检测太脆**：若自动 contact / velocity event 在 BABEL 上不稳定，先加入 BABEL semantic boundary 作 oracle upper bound，再测 rule-based gap。若 gap 太大，说明需要 learnable detector，但这会偏离当前 No-Go。
- **只是工程加速**：必须至少有一个结构化近似分析或强消融证明 event anchor 比 uniform landmark / random landmark 更有本质优势。
- **MAMM full teacher 太慢，无法做足够 pairwise ground truth**：MVP 可只对抽样 pair 运行 full MAMM，其余用 retrieval 指标。
- **DeepPhase baseline 太强**：如果 DeepPhase 在非周期动作上调好通道数后接近 EASGW，则当前 idea 价值下降；此时转向“MAMM scalable tool”而不是“非周期优于 phase”。
- **SIGGRAPH 视觉价值不足**：如果目标投 SIGGRAPH，需要补交互式 motion database demo、sketch-to-candidate retrieval 和 user study；否则按 ICLR 算法论文路线推进。

### 5.4 Potential venue

更适合 **ICLR**，理由是核心是 training-free structured approximation / scalable alignment algorithm。SIGGRAPH 只有在补足可视化工具、动画师检索工作流和大量 qualitative demo 后才有前景。

### 5.5 下一步一周实验

- [ ] 从 BABEL/AMASS 抽 100 条小集，包含 walk/run/kick/jump/sit/turn/pick。
- [ ] 实现 event anchor detector v0：contact on/off、root velocity peak、end-effector velocity zero-crossing。
- [ ] 实现 uniform landmark GW 与 event-anchor EASGW 两个最小版本。
- [ ] 在 30-50 个 pair 上跑 full MAMM / FSUGW 作为 teacher upper bound。
- [ ] 画 speed-error Pareto：full MAMM、DTW、FastDTW、uniform landmark、EASGW。
- [ ] 如果 event anchor 相对 uniform landmark 没有明显 Pareto 优势，立即停止。

## 2026-06-20 temporary convergence (superseded)

DeepSeek 第一轮否掉了 learnable eventized phase representation 作为主线，理由是它像标准 teacher distillation，容易被 DeepPhase / FLD / phase manifold 以及通用 OT representation learning 工作夹击。第二轮一度建议把 MAMM 的真正缺口改写为 **training-free motion alignment at scale**，即 EASGW。

当时临时决策：

> 本 idea pool 条目曾临时主推 EASGW；learnable representation、任意拓扑 retarget、video branch、新 phase 概念全部列为 No-Go。

该判断已被 2026-06-21 reassessment 覆盖。新的最终状态见下节：**parked**。

## 2026-06-21 reassessment: why this direction is parked

### MAMM 的真实工作流边界

对第一个问题的回答是明确的：**是，MAMM 是对单个给定 motion 与单个 control trajectory / control sequence 做 pair-specific optimization。**

更具体地说：

- 输入不是一个 motion database，而是一个已给定的 original motion sequence $X$ 和一个 control sequence $Y$。
- 论文没有解决“从库里自动选哪个 source motion”这个问题；source motion 在实验和应用中需要由用户、资产库或外部逻辑先给出。
- FSUGW 优化得到的是当前 pair 的 transport plan $T$ 和 aligned motion $X'$。
- 每次更换 source motion $X$ 或 control sequence $Y$，都需要重新优化 $T$ 和 $X'$。
- MAMM 的贡献是 **免训练、免跨域映射定义的 pair-level temporal alignment**，不是一个可复用的全局 motion representation / mapping。

这意味着：MAMM 的长处是“给定一个想改的 motion，快速用任意控制序列重排/对齐它”；短处是“不负责帮你从大库中找最该被控制的 motion”。

### 为什么 dataset-level MAMM 的应用动机变弱

用户质疑成立：把 MAMM 扩展到 dataset-level motion matching，目前没有足够强的应用痛点。

原因不是技术上不能做，而是用户价值不清楚：

- **control trajectory 本身是弱 query**：一条 sketch / wave / control curve 可以通过 MAMM 优化对应多个 source motions，因此它不是天然判别性强的检索键。
- **交互直观性不足**：用户找动作时通常更自然地输入 text description、action label、按键、摇杆、目标方向或少量关键帧，而不是先画一条抽象 control trajectory。
- **实时交互已有强路线**：phase 方法、motion matching、learned motion matching 和游戏控制器本来就擅长按键 / root trajectory / style 这类实时输入。
- **加速不等于有用**：EASGW 即使能加速 FSUGW，也主要解决“如何更快跑 pair-specific optimization”，没有回答“为什么要用 control trajectory 做 database retrieval”。

因此，EASGW 不能再写成主推 idea；它只能作为一个 **待应用场景确认的低优先级技术备选**。

### 仍可能成立的窄场景

dataset-level MAMM 只有在很窄的离线专业场景下可能有价值：

- 动画师已有精确手绘曲线、音频节拍、波形或事件时间表；
- 任务要求从资产库里找一个最能被这条控制序列重排的 source motion；
- 输出不要求实时，允许离线 batch search + MAMM refinement；
- text description 太模糊，phase / joystick 控制又不能表达该控制曲线的具体时序形状。

如果找不到这种真实 workflow 和用户证据，本方向不启动。

### 更值得转向的 FSUGW / OT motion 应用候选

DeepSeek 复审后建议保留以下更有痛点的候选：

1. **可学习 FSUGW motion alignment model**  
   目标不是蒸馏一个泛泛 embedding，而是直接学习一次前向输出 alignment / transport plan，替代 pair-specific optimization。它正面解决 MAMM 不可复用和每 pair 重优化的问题。适合 ICLR / NeurIPS；若能做成动画工具，也可考虑 SIGGRAPH。

2. **GW / OT for fine-grained text-motion temporal alignment**  
   用 GW 对齐 motion sequence 与 text token / phrase sequence 的内部结构，减少对帧级标注的依赖。这个痛点比 control trajectory matching 更清楚：text-to-motion 需要细粒度时间对应，但标注稀缺。适合 ICLR / NeurIPS，也可能服务 SIGGRAPH motion generation。

3. **GW-based cross-skeleton retargeting / morphology alignment**  
   用 GW 在不同骨骼结构或不同形态运动之间建立软对应，减少手工关节映射依赖。痛点明确，但与现有 AnyTop、Motion2Motion、WalkTheDog、MoCapAnything 系列会正面竞争，需要非常谨慎定义边界。更偏 SIGGRAPH。

4. **OT sparse plan for motion keyframe extraction / compression**  
   技术可行但价值偏小，作为独立顶会主线不够强；最多作为其他方向的子模块。

5. **dataset-level control matching / EASGW**  
   当前直接降级为否决 / 搁置。除非先证明存在不可替代 workflow，否则不继续。

### Revised decision

当前 note 的最终状态是：

> **parked**。EASGW / dataset-level MAMM 作为主线暂不推进。下一步不应再优化加速细节，而应回到问题定义层，寻找 FSUGW / OT 在 motion 中真正不可替代的应用痛点。
