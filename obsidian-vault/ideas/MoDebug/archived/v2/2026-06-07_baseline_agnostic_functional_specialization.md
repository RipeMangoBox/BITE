---
title: MoDebug Baseline-Agnostic Functional Specialization
created: 2026-06-07T23:23:14+08:00
updated: 2026-06-08T20:45:00+08:00
status: draft
hypothesis: 将 human motion 与 camera motion 统一为离散 token 序列，以文本为 condition，通过 mask-then-predict 范式实现统一的生成与 token-level 编辑——目前无人占据 (Human=Y, Camera=Y, Discrete-Token=Y, Masked-Edit=Y) 的四维交叉点。
source_papers:
  - "[[analysis/ECCV_2022/MotionCLIP_Exposing_Human_Motion_Generation_to_CLIP_Space]]"
  - "[[analysis/ICCV_2023/TMR_Text-to-Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis]]"
  - "[[analysis/ICML_2024/HumanTOMATO_Text-Aligned_Whole-Body_Motion_Generation]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion-Language_Alignment_for_Text-to-Human_Motion_Generation]]"
  - "[[analysis/SIGGRAPH_Asia_2022/PADL_Language-Directed_Physics-Based_Character_Control]]"
  - "[[analysis/CVPR_2023/Trace_and_Pace_Controllable_Pedestrian_Animation_via_Guided_Trajectory_Diffusion]]"
  - "[[analysis/TOG_2023/AdaptNet_Policy_Adaptation_for_Physics-Based_Character_Control]]"
  - "[[analysis/ICLR_2026/AMPED_Adaptive_Multi-objective_Projection_for_balancing_Exploration_and_skill_Diversification]]"
  - "[[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers]]"
tags:
  - MoDebug
  - baseline_agnostic
  - functional_specialization
  - motion_generation
  - mechanism_design
---

# MoDebug Baseline-Agnostic Functional Specialization

> [!abstract] 核心定位
> 本 note 是独立研究分支，不覆盖 [[archived/v1/2026-06-02_modebug_context]] 和 [[archived/v2/2026-06-02_modebug_reboot_plan]] 的 cross-baseline 证据链。这里暂时不关注不同 baseline 的差异，而是先问：如果一个更好的 text-to-motion 模型应当形成可验证的功能分工，我们能否设计一个更通用的训练或 post-train 机制来诱导这种分工，并把它转化为 alignment 与 quality 的提升？

## 1. 研究问题

当前 cross-baseline 结果能提示 layer/stage sensitivity，但如果论文主线完全依赖“某个 baseline 某几层特别敏感”，风险较高：

- baseline 架构不一致，SA/CA/CFG 路径不完全可比；
- 有些模型没有 CA 或 CFG 分支；
- 层敏感曲线可能只是某个 checkpoint 的 pathology，而不是可泛化机制。

因此新增一个更通用的问题：

> [!question] Baseline-agnostic question
> 能否不以 baseline 差异为核心，而把“功能分工”作为 text-to-motion 生成器的结构先验：让模型在 block/stage 层面形成 alignment、global trajectory、tempo/rhythm、local motion、contact/smoothness、diversity 等可验证功能，并通过 pretrain/post-train/routing/evaluator 机制强化这种分工？

该问题的关键不是证明“每一层都有唯一语义角色”，而是证明：

1. 功能分工可以被定义、测量和干预；
2. 被诱导后的分工比自然 emergence 更稳定；
3. 这种分工能带来 alignment、quality 或 robustness 的可复核提升。

## 2. DS max 严肃质询结论

DS max 的核心意见是：这个方向合理，但必须避免“逐层硬绑定”的过强假设。更稳妥的表述是 **block/stage 级 functional decomposition**，允许输入动态路由和软性分工。

可接受的假设：

- 更强的 T2M 生成器可能需要把文本语义、全局运动计划、局部动作细节、物理合理性和多样性控制分配到不同功能子空间或 stage。
- 分工不一定天然清晰，显式诱导可能让模型更容易被 post-train、reward 或 inference repair 控制。
- 对齐和质量不是同一个目标，功能分工可以作为多目标优化的结构化中介。

需要否决的假设：

- 不宣称“每层必须有固定角色”。
- 不宣称“CA 等于 alignment、SA 等于 quality”。
- 不宣称“功能分工越强越好”；过强分离可能降低容量和跨属性协同。
- 不宣称“只要加 MoE 或 router 就是机制贡献”；必须证明功能可测、可控、能提升指标。

## 3. 方法框架：FSD

暂定方法名：**Functional Specialization Distillation / Induction (FSD)**。

FSD 的目标不是绑定某个 backbone 的 layer index，而是在任何 transformer / diffusion / autoregressive T2M backbone 上插入轻量功能支路，并用统一的属性监督和路由正则诱导功能分工。

### 3.0 Input/output/loss 边界

T2M 训练的输入通常是 `text + GT motion`、`text + noised motion` 或 `text + motion tokens`；输出是 reconstructed/generated motion 或 motion tokens。最终评估时，quality 与 alignment 都通过生成 motion 表现出来，因此二者在输出层面天然耦合：

- GT motion 与 text 在数据集标注层面被假定为对齐，reconstruction/diffusion/token CE loss 同时隐含 quality 与 alignment。
- 但隐含对齐不等于显式语义监督。生成模型可能复现训练 motion 分布，却在文本细节、方向、body-part phrase 或 temporal order 上错配。
- 显式对齐 loss 可以来自冻结 CLIP/TMR/T5-like encoder、phrase-action contrast、frame-level semantic label、reward/evaluator 或 preference model。

因此，本路线不把 `FID/R-Precision/TMR score` 简化成一个直接可微的万能 loss，而是区分三层信号：

| 信号                   | 作用                          | 典型形式                                                                 |
| -------------------- | --------------------------- | -------------------------------------------------------------------- |
| Generation loss      | 保持 motion manifold 与重建/去噪能力 | diffusion loss、token CE、VQ recon、velocity/contact loss               |
| Alignment proxy loss | 提供可回传的文本-动作语义监督             | CLIP/TMR cosine、InfoNCE、phrase-action contrast、frame semantic cosine |
| Evaluator/reward     | 对生成结果做后训练或 rerank           | TMR score、attribute critic、reward/value guidance、preference          |

主流工作并非从未使用显式对齐：MotionCLIP 用 CLIP 余弦对齐，TMR 联合生成与 InfoNCE retrieval，HumanTOMATO 用 TMR 文本先验和显式对齐监督，MoLingo 用帧级文本标签余弦损失训练 SAE。更准确的边界是：很多 generator 不直接把完整 evaluator 的 R-Precision/TMR 排名指标作为主训练 loss，原因包括 batch-level retrieval 指标非平滑或不可直接回传、外部 evaluator 冻结后可能带来 domain bias、对齐 loss 会与 motion quality/reconstruction 冲突、计算开销较高、以及过度优化评估器导致 reward hacking 或 eval unfairness。可行做法是把对齐作为低权重 proxy 或 post-train reward，而不是取代 motion generation loss。

### 3.1 模块

- Backbone：保持原 T2M 生成器主体不变，优先先冻结主干做 post-train MVP。
- Functional experts：在若干 stage 后插入轻量 expert，例如 2-layer MLP、adapter、LoRA branch 或小 attention block。
- Router：根据 hidden state、text embedding、timestep、layer/stage id 输出 soft weights。
- Attribute probes：不直接参与主生成时也可作为诊断器，预测 alignment、trajectory、tempo、contact、smoothness、diversity 等属性。
- Optional evaluator：把 intervention 失败样本训练成 attribute critic，用于 rerank、reward fine-tune 或 preference optimization。

### 3.2 推荐的功能专家

| Expert          | 目标功能                                           | 监督或代理信号                                                           |
| --------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| AlignExpert     | 文本动作语义、body-part phrase、方向/速度词进入 motion latent | text-motion matching、phrase-action contrast、caption attribute tag |
| GlobalExpert    | root trajectory、全局位移、朝向、动作阶段结构                 | root path、velocity envelope、trajectory error                      |
| RhythmExpert    | tempo、周期性、动作节奏                                 | speed periodicity、step frequency、duration-normalized velocity     |
| LocalExpert     | 局部关节动作、body part coordination                  | joint-group velocity、left/right consistency、local jerk            |
| PhysicalExpert  | foot contact、滑步、平滑性、plausibility               | contact labels、foot skating score、acceleration/jerk smoothness    |
| DiversityExpert | 同文本多样性与 mode coverage                          | multi-seed variance、MModality、diversity proxy                     |

MVP 不需要全上。第一阶段建议只做 `AlignExpert` + `PhysicalExpert/LocalExpert` 两个专家，避免设计过重。

### 3.3 AC3D-style condition scope as secondary reference

[[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers|AC3D]] 只能作为与 Bailando 同级的旁证，不能作为 MoDebug 主线。原因是 AC3D 的输入是 `text + camera`，其中 camera 是额外低频控制条件，可以相对清楚地与 text/content 分工；而 T2M 的输入通常只有 `text`，输出 motion 同时承载动作质量和文本对齐，不能把 camera-control 的主次条件结构简单映射成 quality/alignment 分工。除非先证明 motion quality 与 text alignment 的可操作解耦，否则不应把 AC3D 的前 40% 去噪步或前 8 层注入策略直接迁移到 T2M。

AC3D 对 MoDebug 的可用价值应收缩为一种诊断提醒：**先观察控制/语义/质量信号在哪些 layer 或 diffusion step 上可测，再决定是否需要限定作用域**。它只支持提出补充 probe，不支持直接提出 FSD 主方法。

对应到当前接力，AC3D 更适合启发两个补充诊断：

- **LDO: Layer Direct Output**：用分块后的少数 layer output 直接解码或接评价头，检查不同 stage 的 hidden state 是否已经包含可用的 motion quality / text alignment 信息。
- **DSO: Diffusion Step Output**：仅对 diffusion baseline，保存若干 denoising step 后的 motion output，观察 alignment、trajectory、local quality、smoothness 等指标在哪些 step 开始形成或恶化。

因此 AC3D 不进入 FSD 的核心 claim，只作为“补充 LDO/DSO 诊断有必要”的参考。真正的主线仍应由 T2M 自身的 layerwise intervention、LDO/DSO 指标和 post-train 消融来决定。

## 4. 主方案

### 4.1 Post-train FSD-MVP

先选择一个可控 backbone，冻结原始生成器，仅训练零初始化 adapters / LoRA branches / optional router。MVP 不是直接追求跨 baseline 通用收益，而是验证一个核心设想：**在不破坏原 motion manifold 的前提下，stage-wise post-train 能否定向改善 alignment 或 quality 敏感区。**

最小结构：

- Frozen base：冻结 backbone 主干，保留原生成路径。
- Stage adapters：在 2-4 个候选 stage 后加入零初始化 residual adapters，初始行为与 checkpoint 等价。
- K=2 functions：`AlignAdapter` 与 `LocalQualityAdapter`；MVP 可先不引入 MoE router，而是手动指定或规则化选择 stage。
- Optional router：第二阶段再让 router 根据 hidden state、text embedding、timestep 或 phase score 给 adapters 加权。
- 输出：`h_out = h + gamma * adapter(h, c)`，其中 `gamma` 初始为 `0` 或很小值，采用 warmup，避免破坏原模型。

Baseline 选择：

- 第一版必须先选一个最可控 backbone，而不是四个 baseline 同时做。优先标准是训练脚本可控、evaluator 完整、可复用现有 intervention 发现敏感区。
- 如果沿当前结果，MotionCLR 适合验证 CFG_CA / alignment-quality coupling；MoLingo 适合验证显式 motion-language alignment 和 FID_TMR/R-Precision 分离；MotionGPT/MotionStreamer 更适合作为后续架构对照。
- 论文表述仍可保持 baseline-agnostic：方法定义不依赖某个层号，但 MVP 需要在一个 backbone 上先证明机制。

Stage 选择策略：

| 策略               | 做法                                                                                | 用途                |
| ---------------- | --------------------------------------------------------------------------------- | ----------------- |
| Manual           | 用已有 layerwise intervention 选择敏感 block，例如 MotionCLR CFG_CA 12-15 或 late SA spike   | 最快验证机制，不伪装成自动化    |
| Probe-guided     | 对每层记录 alignment proxy、quality proxy 与 intervention degradation，选 Pareto 高风险 stage | 半自动扩展到第二 baseline |
| Adapter-scan     | 插入 zero-init adapters 后短程训练，比较每个 stage 的 validation gain / drift                  | 需要额外 compute，但最直接 |
| Learnable router | router 根据 text/phase/timestep 动态选择 adapter                                        | 第二阶段机制，不作为第一版 MVP |

训练目标：

- `L_gen`：原始 diffusion / autoregressive / token CE 目标，用于保持生成分布。
- `L_align`：冻结 TMR/CLIP/MoLingo-style semantic encoder 的 cosine 或 InfoNCE proxy，低权重使用；不直接把 R-Precision 排名当可微主 loss。
- `L_quality`：contact、smoothness、local jerk、trajectory consistency 等 motion attribute loss。
- `L_load`：router 负载均衡，防止只走一个 expert。
- `L_sep`：不同 expert 输出的相关性或 CKA 相似度惩罚，防止专家同质化。
- `L_preserve`：冻结主干时限制输出偏离 baseline，避免 post-train 把已有质量破坏掉。

一个可执行的总目标：

```text
L = L_gen
  + lambda_align * L_align
  + lambda_quality * L_quality
  + lambda_load * L_load
  + lambda_sep * L_sep
  + lambda_preserve * L_preserve
```

推荐初始权重：

- `lambda_align = 0.05`
- `lambda_quality = 0.05`
- `lambda_load = 0.01`
- `lambda_sep = 0.01`
- `lambda_preserve = 0.1`

这些不是最终超参，作用是让第一版验证不会强行改写主干表示。

### 4.3 Bailando-style stage-wise post-train 借鉴

Bailando 可作为 stage-wise post-train 的重要先例，但需要准确类比：它不是“每层分别成为 actor/critic”，而是把 Motion GPT 的前 6 个 Transformer layers 视为 frozen state network，把后 6 层加 linear-softmax 视为 policy-making actor，并额外添加 3-layer Transformer critic，用 beat-align reward 和 half-body consistency reward 做 actor-critic finetune。

对 MoDebug 的借鉴：

- State network：冻结早中层或已证明主要负责 motion manifold 的 stage，保持原模型生成能力。
- Actor network：只开放中后层 adapters / LoRA / policy head，使 post-train 主要改变条件响应和局部修复能力。
- Critic/reward：用冻结 evaluator 或 attribute critic 给 sequence-level / phase-level reward，例如 text-motion similarity、contact、smoothness、root trajectory、diversity penalty。
- Small LR + preserve loss：借鉴 Bailando 和 AdaptNet，post-train 必须小步、零初始化、保留原行为。

不能过度类比的点：

- Bailando 对齐对象是 music beat，不是自然语言语义；T2M 需要防止 reward 只优化 retrieval 而破坏 motion quality。
- Bailando 的 actor/critic 划分依赖其 12-layer GPT 和离散 code sequence；diffusion/flow/continuous latent 模型需要按 denoising stage、latent block 或 decoder stage 重定义。
- Bailando 的 reward 较明确，T2M 的 alignment reward 更容易受 evaluator bias 和文本歧义影响。

DS max 多轮审查后的处理原则：

- Bailando 只作为“stage-wise post-train 可以成立”的间接先例，不证明 MoDebug 的 diagnosed sensitive stage 一定适合 post-train。
- 第一版 MVP 不混入 actor-critic RL，避免把核心问题从“诊断选层是否有效”变成“reward/RL 是否调好”。
- 若 supervised adapter MVP 失败且原因是 rule-based weights 僵硬，再考虑 critic-guided dynamic weighting；若原因是 adapter 容量不足，再考虑 LoRA 或只微调 sensitive stage。

### 4.2 为什么先做 post-train

post-train 比 pretrain 更适合作为 MVP：

- 成本低，可以复用已有 checkpoint 和 evaluator；
- 可以直接回答“功能分工是否能修复已训练模型的 alignment/quality trade-off”；
- 失败时可定位是专家设计无效、loss 不合适，还是假设本身不成立；
- 成功后再扩展到 pretrain stage-aware objectives 更有说服力。

## 5. 备选机制

| 方向                             | 做法                                                                                           | 适合何时使用                                         |
| ------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Pretrain stage-aware objective | 在训练早期就给不同 stage 加 trajectory、alignment、contact、smoothness 辅助目标                               | post-train MVP 有正信号后，用于证明机制不是 checkpoint patch |
| Routing/MoE                    | 把 FFN 或 adapter branch 替换为 soft/top-2 experts，按 text attribute、timestep、motion complexity 路由 | router 权重与属性有稳定相关时推进                           |
| Pure regularization            | 不加 experts，仅用 CKA/MI/orthogonality 约束不同 stage 表示差异                                           | 参数预算极小，或 experts 带来 FID 退化时                    |
| Evaluator/reward/preference    | 用 intervention 失败样本训练 attribute critic，做 rerank、reward fine-tune 或 DPO-like post-train       | attribute evaluator 与人工/标准指标相关性足够高时            |
| Inference-time repair          | probe 发现某次采样进入坏状态时，触发 adaptive CFG、layer patch 或 resample                                    | 作为工程上限或 ablation，不宜作为主贡献                       |

## 6. 可验证预测

如果 FSD 假设成立，应至少出现以下部分现象：

1. Alignment 指标提升，且 quality 不被牺牲：R-Precision / Matching 改善时，FID/FID_TMR、smoothness、contact 不显著变差。
2. Router 与输入属性相关：动作复杂、body-part 明确或速度词明显的 prompt 应激活不同 expert 组合。
3. Expert 表示可分：expert 输出之间 CKA/余弦相似度下降，attribute probe 的线性可分性提高。
4. 干预鲁棒性提高：对已知敏感 stage 做 SA/CA/CFG 或 hidden-state perturbation 时，FSD 模型的退化小于 baseline。
5. Trade-off 可控：如果 quality 与 alignment 冲突，router 或 reward 能给出可解释的选择，而不是随机牺牲一个指标。
6. 作用域诊断可测：LDO/DSO 能补充说明哪些 layer 或 diffusion step 已经携带 alignment/quality 相关信息；但这只是诊断证据，不直接等价于 condition 注入策略。

## 7. 最小实验设计

### 7.1 MVP 配置

| 项目       | 配置                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------- |
| Backbone | 先选一个最可控、已有 evaluator 的 T2M backbone；若沿当前 MoDebug，优先 MotionCLR 或 MoLingo 中实现成本最低者                        |
| 数据       | HumanML3D train/test；先用小步 post-train，不重训全模型                                                             |
| 参数       | 冻结 backbone，只训练 zero-init stage adapters；router 暂缓                                                      |
| 插入点      | 从已有 layerwise intervention 选 1 个敏感 block + 1 个非敏感 block 作对照                                             |
| 训练       | 直接 post-train 2k-10k steps；只有 probe/evaluator 不可用时才补前提 eval                                             |
| Loss     | `L_gen + low_weight L_align + L_quality + L_preserve`；先不加 `L_sep/L_load`                                |
| Eval     | 官方 FID/R-Precision/Matching + frozen TMR/CLIP similarity + contact/smoothness + intervention robustness |

诊断稳定性必须记录：

- layerwise sensitivity 排名在不同 seed / prompt slice / validation subset 下的 Kendall tau；
- 每层 intervention 后 FID、R-Precision、Matching 的均值和方差；
- sensitive stage 与 neutral stage 的分离 margin；
- 若 `tau < 0.5` 或 separation margin 不稳定，则不得进入 post-train 结论，只能报告诊断不稳定。

### 7.2 对照组

必须包含以下 ablation，否则不能证明“功能分工”而不是“加参数”：

| 对照                                                     | 目的                                                                            |
| ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Frozen baseline                                        | 原模型指标                                                                         |
| Same-params adapter, no routing                        | 排除只是参数量增加                                                                     |
| Random routing                                         | 排除 router 只是噪声正则                                                              |
| Shared expert                                          | 排除 expert 分化不是必要条件                                                            |
| FSD full                                               | 主方法                                                                           |
| FSD without `L_sep`                                    | 检查分离约束是否必要                                                                    |
| FSD without attribute loss                             | 检查属性监督是否必要                                                                    |
| Sensitive stage adapter vs neutral stage adapter       | 验证 layer/stage 选择是否真实重要                                                       |
| LDO by coarse layer blocks                             | 检查不同 stage direct output 是否已经携带可解码的 alignment/quality 信息                              |
| DSO by diffusion step blocks                           | 仅对 diffusion baseline，检查生成指标随 denoising step 的形成轨迹                                  |

### 7.3 成功标准

MVP 不要求 SOTA，但至少要满足：

- 主指标：R-Precision Top3 或 Matching 有稳定改善，FID/FID_TMR 不显著恶化；
- 属性指标：contact/smoothness/local jerk 至少一个改善，且不靠 motion 静止化作弊；
- 表示指标：expert 输出相似度下降，router entropy 不 collapse；
- 鲁棒性：在同一 intervention eval 下，敏感层退化幅度小于 frozen baseline；
- 消融：FSD full 优于 same-params adapter 和 random routing。
- 关键一针见血验证：sensitive stage adapter 的 post-train 收益必须优于 neutral stage adapter，否则 layer/stage specialization 叙事不成立。

DS max 后的硬失败标准：

- sensitive adapter 不显著优于 neutral/random adapter；
- rule-based token/phase weights 不优于 uniform weights；
- alignment proxy 提升但 FID/contact/smoothness 明显退化；
- 诊断稳定性不足导致 sensitive stage 无法复现。

## 8. 风险与 pivot

| 风险                         | 严重程度 | 必须解决/可绕过 | 处理方案                                                                             | Pivot                                                  |
| -------------------------- | ---- | -------- | -------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 分工更清晰但指标不升                 | 高    | 必须解决     | 对比 same-params adapter，确认是否只是解释性现象                                               | 转为 interpretability paper，降低 quality-improvement claim |
| FID 变差                     | 高    | 必须解决     | 提高 `L_preserve`，降低 expert residual `gamma`，只插更少 stage                            | 改做 inference-time repair 或 pure regularization         |
| Router collapse            | 中    | 必须解决     | 增大 `L_load`，使用 entropy floor 或 top-2 routing                                     | 固定 stage routing，减少动态路由自由度                             |
| Attribute loss 监督噪声大       | 中    | 可绕过      | 用更稳定的 proxy，如 contact/smoothness/root velocity                                   | 暂时只做 alignment + preservation                          |
| Reviewer 认为只是 MoE/adapters | 高    | 必须解决     | 强化 functional probes、intervention robustness、attribute-specific ablation         | 叙事改为 diagnostic-to-training pipeline                   |
| 跨 backbone 不泛化             | 高    | 必须解决     | 先 claim baseline-agnostic framework，不 claim universal gain；至少补第二 backbone sanity | 聚焦单 backbone 的机制论文，避免 universal 方法 claim               |
| 对齐 reward hacking          | 高    | 必须解决     | 对齐 proxy 与 FID/contact/smoothness/human check 同时监控，限制 `lambda_align`             | 只保留对齐 loss 为 probe/reward，不进入主训练                       |
| 组件过多导致不可解释                 | 高    | 必须解决     | MVP 暂缓 router/MoE，先做 zero-init adapters + 规则 stage selection                     | 将 FSD 收缩为 stage-wise post-train adapter                |

## 9. Top-tier 叙事

保守但有潜力的叙事：

> Text-to-motion generation suffers from entangled control of text alignment and motion quality. We propose a baseline-agnostic functional specialization framework that induces soft stage-level decomposition into alignment and motion-quality experts. The resulting model is not only better on standard generation metrics, but also more interpretable and robust under causal intervention.

中文版本：

> T2M 模型的文本对齐和动作质量往往被纠缠在同一表示流中。MoDebug-FSD 把“功能分工”从事后诊断变成可训练机制：通过轻量专家、动态路由和属性级约束，诱导模型形成可测、可控、可消融的 alignment-quality 分工，从而提升标准指标和干预鲁棒性。

这个叙事的关键证据链应是：

1. 现有 intervention 说明 alignment-quality entanglement 存在；
2. FSD 提供 baseline-agnostic 的分工诱导方法；
3. 分工可以被 probes 和 router statistics 验证；
4. 分工不是只提升可解释性，而是改善 alignment/quality 或 robustness；
5. 消融证明收益不是简单参数量或 MoE trick。

## 10. 必须否决的过强说法

- 不写“理想模型每层都应该有不同分工”。
- 不写“我们发现了所有 T2M 模型统一的层语义图谱”。
- 不写“SA/CA 与 quality/alignment 一一对应”。
- 不写“功能分工越强越好”；过强分离可能破坏协同。
- 不写“无需 baseline 差异实验”；baseline 差异仍用于诊断和压力测试，只是不作为新分支的主假设。
- 不写“通用方法必然跨 backbone 提升”；最多先写 baseline-agnostic design，跨 backbone 泛化需要实验支持。

## 11. 执行路线

| 阶段      | 目标             | 实验                                                                             | 成功标准                                                   | Pivot                                 |
| ------- | -------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------- |
| Phase 0 | 确认属性 probe 可用  | contact/smoothness/root trajectory/semantic matching probe sanity              | probes 与官方指标或人工抽检方向一致                                  | 先修 evaluator，不进入 FSD 训练               |
| Phase 1 | Post-train MVP | 冻结 backbone，K=2 experts，2-4 个中后 stage，5k-20k steps                             | 指标不降，router 不 collapse，FSD full 优于 same-params adapter | 改小 `gamma`、减少 stage、调低 auxiliary loss |
| Phase 2 | 机制验证           | intervention robustness、expert swap、router ablation、attribute-specific prompts | FSD 对敏感干预更鲁棒，expert 角色可预测                              | 若只解释不提质，转 interpretability 叙事         |
| Phase 3 | 扩展             | 第二 backbone 或第二数据集 sanity                                                      | 至少一个独立设置复现趋势                                           | 收缩为单 backbone 机制论文                    |
| Phase 4 | 训练侧升级          | pretrain stage-aware objective 或 reward/preference post-train                  | 比 post-train MVP 更稳定或更高上限                              | 若成本过高，保留为 future work                 |

## 12. 与当前 MoDebug 的关系

这条路线不否定当前 baseline eval，反而把它们转成两个用途：

- 作为诊断证据：说明自然模型确实会出现 layer/stage sensitivity 和 alignment-quality coupling。
- 作为压力测试：FSD 训练后复跑相同 intervention，验证模型是否更稳、更可控。

因此，MoDebug 可以形成两层结构：

1. **Diagnosis layer**：cross-baseline attention intervention 发现 sensitivity 与 coupling。
2. **Mechanism layer**：FSD 把 diagnosis 转成 baseline-agnostic 的训练与 post-train 机制。

如果 FSD MVP 成功，论文主线可从“某些层很敏感”升级为“诊断揭示了 entanglement，功能分工诱导能缓解 entanglement 并提升 T2M 生成”。
