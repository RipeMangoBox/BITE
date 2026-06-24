---
title: MoDebug Reboot Plan
created: 2026-06-02T00:00:00+08:00
updated: 2026-06-07T23:12:41+08:00
status: active
hypothesis: "Cross-baseline attention intervention 用于诊断 text-motion alignment 与 motion generation quality 的学习机制，并反推出 post-train/pretrain/routing/regularization 机制；Trace 3 数据效率和训练侧策略作为机制落地路径之一。"
tags:
  - MoDebug
  - reboot
  - trace_1
  - trace_2
  - trace_3
---

# MoDebug Reboot Plan

> [!abstract] 唯一主计划
> 本文只定义研究设计、Trace 分工和决策关口。当前状态见 [[archived/v1/2026-06-02_modebug_context]]；实验索引见 [[experiments/README]]，跨 baseline 门禁见 [[experiments/archived/v2/2026-06-03_cross_baseline_ca_cfg_gate]]。

## 2026-06-07 Plan Update

MoDebug 当前主问题调整为：**如何从逐层学习机制诊断中提高 text-motion alignment 和 motion generation quality**。四个 baseline 的 eval 是为了提供因果诊断信号，而不是为了比较模型强弱或追求完全同构的指标重构。

### 当前证据面

| 证据 | 已观察到什么 | 对机制设计的含义 |
|---|---|---|
| MotionCLR CFG_CA | 12-15 层出现强退化，Top1/Top2/Top3 和 Matching 同时受损 | CFG cross-attention 或 cond/uncond boundary 在中后层可能承载 alignment-quality 关键耦合，适合做 targeted post-train 或 layer-specific regularization。 |
| MotionCLR SA/CA/CFG_SA | 大多数层接近 baseline，部分 late layer 有 FID spike | 质量敏感性可能集中在少数 stage，而不是每层独立分工；需要 block-level 而非 single-layer-only 解释。 |
| MotionGPT SA/CA | 与 baseline 接近，CFG family 架构 unsupported | 稳定性可作为冗余/鲁棒对照；需要避免把“无退化”直接解释为“无机制”。 |
| MoLingo CFG_SA/CFG_CA | FID_TMR 上升但 Top1/Top2/Top3 较稳定 | motion distribution quality 与 text retrieval alignment 可分离，应设计双目标机制而不是只优化 R-Precision。 |
| MotionStreamer | encode-cache SA/CFG_SA 正在运行 | 用于验证无 CA 模块的 causal self-attention 架构是否也出现 stage-level 敏感性。 |

### 新的机制设计问题

1. Alignment mechanism：哪些层或模块决定文本语义是否正确进入 motion latent？需要 token/phrase-level probe，而不仅是 R-Precision。
2. Quality mechanism：哪些层或模块决定 motion distribution、physical plausibility、foot contact、smoothness 和局部高频质量？需要 FID/FID_TMR 外的 motion attribute evaluator。
3. CFG mechanism：cond/uncond branch 在哪些层产生有用差异，哪些层替换会破坏对齐或质量？需要 layer-specific CFG consistency 或 branch disentanglement。
4. Training mechanism：如果某些 stage 的职责稳定存在，应考虑 pretrain/post-train/routing/regularization，而不是只做 inference-time intervention。

### 候选机制方向

- Post-train layer-specific regularization：对已识别的敏感 stage 增加 alignment consistency、CFG branch consistency 或 quality-preserving loss，优先针对 MotionCLR CFG_CA 12-15 层做最小验证。
- Pretrain stage-aware objectives：早层/中层/晚层分别加入全局轨迹、文本动作语义、物理接触/平滑等中间任务，让分工从训练中形成，而不是靠事后解释。
- Conditional routing 或 MoE：按动作词、身体部位、速度/节奏、CFG scale 或 timestep 路由到不同专家，目标是减少 text semantics、global trajectory 和 local quality 的冲突。
- Intervention-guided evaluator training：把逐层干预产生的失败样本作为诊断数据，训练 attribute critic 或 preference/reward，用于后续 post-train。
- Block-level specialization metric：用 probe、swap/restore、layer freeze 和 counterfactual training 定义“分工是否真实有益”，避免仅凭 FID 曲线宣称机制。

### DS max 后的最小处理集合

1. MotionCLR 12-15 层单层化：对 CFG_CA 12、13、14、15 分别做 activation patching、swap/restore 和 CFG scale sweep。验证目标是确认退化来自单层核心点、连续 block 耦合区，还是 CFG scale 放大后的路径错配。
2. Alignment 与 quality 拆分：在已有 FID/R-Precision/Matching 外补 attribute probes，至少覆盖 semantic alignment、global trajectory、tempo/rhythm、body part/local motion、foot contact、smoothness、diversity。验证目标是把“FID 退化”拆成可训练的 motion 属性。
3. MoLingo 质量退化定位：对 CFG_SA/CFG_CA 的输出做帧段级和属性级分析，检查 FID_TMR 退化是否集中在 transition/contact/smoothness/diversity，而不是文本语义错配。
4. MotionGPT 可观测性复核：优先做 representation probing；若仍无信号，再做更强 stress test。目标是区分“架构鲁棒/冗余”和“当前干预不适配”。
5. MotionStreamer 完成后只补 SA/CFG_SA 证据，不补不存在的 CA/CFG_CA；它用于检验 causal self-attention 架构是否也有 stage-level 敏感性。

### 机制验证矩阵

| 方向 | 最小验证实验 | 成功标准 | 主要风险 |
|---|---|---|---|
| Post-train regularization | 在 MotionCLR 12-15 层加入 CFG branch consistency、alignment consistency 或 quality-preserving loss，小步 fine-tune 后复跑同一 eval | CFG_CA 退化下降，同时 baseline FID/R-Precision 不显著变差 | 只修复一个 backbone 的 CFG pathology，无法泛化。 |
| Pretrain stage-aware objective | 早层加 global trajectory/tempo 目标，中层加 text action/body-part 目标，晚层加 contact/smoothness 目标；先用小规模 ablation 验证 | probe 显示 stage 属性分工更清晰，正式指标至少一项 alignment 或 quality 改善且无明显 trade-off | 辅助目标可能人为制造分工但不提高生成质量。 |
| Routing/MoE | 按动作词、身体部位、速度/节奏、timestep 或 CFG scale 做 stage-aware routing；先只在敏感 block 加门控 | 对 hard prompt 或敏感层干预的鲁棒性提升，参数/延迟增加可控 | 路由学习不稳定，或变成 prompt-type overfitting。 |
| CFG-specific repair | 对 cond/uncond branch 做 layer-specific scale、feature norm alignment 或 late-layer CFG attenuation | MotionCLR CFG_CA 12-15 的 FID、Matching、Top1 同时回收 | 可能降低 CFG 的文本遵循能力，需 hard prompt 检查。 |
| Evaluator/reward/preference | 用干预失败样本训练 attribute critic 或 preference model，再做 rerank、reward fine-tune 或 DPO-like post-train | 质量属性提升不依赖 R-Precision 假阳性，human/automatic attribute 一致 | evaluator bias 会被模型利用，需 held-out 属性和人工抽检。 |
| Inference-time diagnostic/repair | 用 probe 预测某次采样是否进入敏感坏状态，触发 layer patch、resample 或 adaptive CFG | 不训练主模型即可降低失败率，且速度开销可接受 | 容易成为工程补丁，paper 机制贡献较弱。 |

### 属性 probe 优先级

- P0：semantic alignment probe，输入为 12-15 层隐藏状态或 attention readout，监督用 text-motion matching / phrase-action 对；用于验证 CFG_CA 退化是否真与语义对齐相关。
- P0：contact / smoothness probe，优先看 late SA 与 CFG_SA spike 层；用于确认 FID spike 是否来自物理 plausibility 或局部高频质量。
- P1：global trajectory 与 tempo/rhythm probe，用 root path、速度、周期性步态特征监督；用于区分全局运动计划和局部 motion refinement。
- P1：body part / local motion probe，用关节组速度、左右肢体动作、局部 jerk 监督；用于分析文本中 body-part phrase 是否进入对应 motion 子空间。
- P1：diversity probe，用同 prompt 多 seed 方差和 mode collapse proxy 监督；用于解释 MoLingo 的 FID_TMR 退化是否来自 diversity，而不是语义错误。

### Paper 叙事收敛

保守但有潜力的主线是：**attention intervention reveals functional alignment-quality coupling regions in text-to-motion generators, and these regions can be converted into trainable controls for post-training and pretraining**。这个叙事允许模型间差异，也允许 MotionGPT/MotionStreamer 作为架构对照。

需要否决的过强叙事：

- 不宣称“每层都有独立语义分工”。
- 不宣称“CA 专门负责 alignment、SA 专门负责 quality”；当前更像 stage-level coupling，而不是模块一一对应。
- 不宣称“MoLingo 已证明 quality 与 alignment 完全解耦”；目前只是指标敏感性分离。
- 不宣称“MotionGPT 无层分工”；当前只是 SA/CA intervention 无明显指标退化。

### 决策边界

- 不把当前 layerwise 曲线直接写成“每层语义分工已被证明”。
- 不把 Top3 稳定解释为模型质量稳定；MoLingo 已显示 FID_TMR 与 R-Precision 可能分离。
- 优先寻找能同时提升 alignment 和 quality 的机制；如果两者冲突，必须明确 trade-off 并设计多目标选择。
- Top-tier 潜力来自“可证伪的机制定义 + 跨 baseline 复现 + 可训练改进”，不是来自单一 baseline 的调参修复。

## 1. Reboot 原因

原 MoDebug v1 的“文本传播追踪”失败根因：

| 根因                   | 说明                                                              |
| -------------------- | --------------------------------------------------------------- |
| 文本是广播注入              | 每个 denoising step、每个 CA layer 接收同一 text embedding；不存在可追踪的逐层传播链。 |
| 全局扰动指标错位             | `relative_l2` 不能定位 token/span 到 time/body 的局部语义错绑。              |
| failure label 不是机制标签 | `left_right_error` 等输出症状不能直接映射到某层 attention 机制。                 |
| null 条件不稳定           | semantic null、standing、zero_text 语义不同。                          |

## 2. Trace 分工

| Trace   | 对应 Line | 旧称      | 目标                       | 当前决策    |
| ------- | ------- | ------- | ------------------------ | ------- |
| Trace 1 | Line 1  | Track B | CA 层 CFG/CA output 扰动诊断  | diagnostic_completed  |
| Trace 2 | Line 2  | Track C | 语义动作表征                   | demoted |
| Trace 3 | Line 3  | Track A | DispLoss + 数据增强 / 训练数据效率 | active  |

优先级：Trace 3 与 Trace 1 并行；Trace 2 只保留参考资料。

## 3. Trace 1 — CA 层扰动诊断

### 目标

不再问“文本传播到哪里”，而是问“文本条件在第几层起作用”。核心假设是不同 CA/CLR 层对 text-motion alignment 的贡献不同。

### 正式设计

- Testbed：首选 MotionCLR release checkpoint；备选 MoLingo。
- 目标层：MotionCLR 18 个 `CLRBlock` 的 `ResidualCLRAttentionLayer.cross_attention`。
- 正式 Line 1 至少包含两类逐层实验：
  - CA output perturbation：逐层包装 cross-attention forward，输出 `alpha * original_ca_output`。
  - CFG-faithful uncond replacement：逐层在官方 CFG 拼接 batch 内，把条件半边该层输出 hidden state 替换为同 batch 的 uncond 半边 hidden state；其余层保持正常 cond 路径，最后仍按官方 CFG cond/uncond 拼接公式出样。
- 组数下限：18 层 × 2 类逐层实验 = 至少 36 组，不含 baseline、no-op、all-layer positive control。
- 必须保留 self-attention、FFN、residual、time embedding 路径。
- 控制组：
  - no-op：`alpha=1`，必须与未 hook baseline 逐位一致。
  - positive control：所有层 `alpha=0`。
  - 连续扰动：`alpha ∈ {0, 0.25, 0.5, 0.75, 1}`。
  - CFG no-op：条件半边替换逻辑关闭时必须与官方 CFG baseline 逐位一致。
  - CFG all-layer uncond replacement：所有层条件半边 hidden state 均替换为 uncond 半边，作为 positive control。

### 通过条件

- [x] DS 批准正式 hook 和命令。
- [x] no-op 等价验证通过。
- [x] 18 层逐层 CA output perturbation 完整落盘。
- [x] 18 层逐层 CFG cond-half uncond replacement 完整落盘，且 CFG split/index 无错位。
- [x] 至少一层显示明显数值扰动；formal diagnostic 结论见 [[experiments/motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。
- [ ] 层级差异需在后续 qualitative motion inspection 或 evaluator subset 中排除纯数值敏感假阳性；当前不写 paper-level 指标。

## 4. Trace 2 — 语义动作表征

该方向降级为参考，不投入当前双卡测试。

原因：

- Motion 域没有 DINOv2 级别 frozen semantic encoder。
- MoLingo SAE、COME/MoCMAE、MotionCLR、MotionCLIP 等方向已有多人并行。
- 解决“motion DINO”本身是一篇独立论文体量。

重新激活条件：Trace 1/3 形成结果后，有独立证据表明某 motion encoder 足够强，且存在明确差异化角度。

## 5. Trace 3 — 数据效率训练侧

### 目标

在真实 HumanML3D + MotionCLR 训练路径上，验证训练正则和数据策略是否能带来可复核增益。当前不 claim motion 数据增强新颖；只 claim 具体 policy 在具体 backbone/split/evaluator 下的有效性或无效性。

### 正式设计

四组对比：

| 条件               | 说明                                                      |
| ---------------- | ------------------------------------------------------- |
| Baseline         | MotionCLR 原始训练。                                         |
| + Augmentation   | 明确 policy，例如 mirror、temporal scale、root yaw；必须有语义一致性约束。 |
| + DispLoss       | 明确 hook 层、`lambda`、`tau`、feature shape。                 |
| + Aug + DispLoss | 联合条件。                                                   |

正式指标：FID、R-Precision、Matching Score、训练收敛曲线。任何 smoke/path-validation loss 都不得填入正式指标表。正式 Line 3 必须是真训练 run；3-step debug/path validation 只能验证代码路径，不能代表训练完成。

### 通过条件

- [ ] DS 批准训练循环 patch、DispLoss/augmentation 代码和命令。
- [ ] baseline 等价测试通过：新增 flag 关闭时与原 baseline 一致。
- [ ] 训练循环能精确停在指定 step，checkpoint 写盘可控。
- [ ] 正式实验中 DispLoss 或 augmentation policy 在指标上有可复核改善，且不破坏文本语义一致性。

## 6. 已完成的双卡 bounded validation

这一步已完成，但不是正式实验：

| GPU  | Trace   | 目的                                                         | 输出状态                          |
| ---- | ------- | ---------------------------------------------------------- | ----------------------------- |
| GPU1 | Trace 1 | 验证 CA output scaling hook 的 no-op 等价与 positive control 可运行 | `engineering_validation_only` |
| GPU0 | Trace 3 | 验证真实 HumanML3D batch、真实 MotionCLR update、精确步数停止            | `engineering_validation_only` |

bounded validation 使用真实数据和真实 checkpoint，但只验证代码/命令可控性，不产生正式结论。Trace 1 的 36+ 组 formal diagnostic 已完成；Trace 3 仍需等待真实训练消融和 official evaluator。

## 7. 正式实验门禁

- [ ] 代码 diff、命令、配置、数据/权重路径、控制组、成功/失败标准提交 DS。
- [ ] DS 返回 `APPROVED` 或针对 bounded validation 的明确批准。
- [ ] run 目录不复用历史 smoke/probe 目录。
- [ ] manifest 启动前记录 git head、dirty diff、命令、seed、dataset、checkpoint/evaluator SHA256、软件/硬件环境。

## 8. 相关入口

- [[trace_1_ca_perturbation/README]]
- [[trace_2_semantic_repr/README]]
- [[trace_3_data_efficiency/README]]
- [[experiments/README]]
- [[experiments/motionclr/2026-06-02_ds_formal_experiment_gate]]
- [[experiments/motionclr/2026-06-02_dual_trace_supervision]]
- [[experiments/motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]
