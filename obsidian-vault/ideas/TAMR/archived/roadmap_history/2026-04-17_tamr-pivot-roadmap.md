---
created: 2026-04-17
updated: 2026-04-19
status: active
title: "TAMR Pivot Roadmap: Event-Grounded Fine-Grained Motion-Text Matching"
tags:
  - tamr
  - motionpatches
  - roadmap
  - iclr2027
  - fine-grained
  - event-grounded
---
# TAMR Pivot Roadmap: Event-Grounded Fine-Grained Motion-Text Matching

> 本文档取代 `2026-04-15_tamr-status-and-roadmap.md`（已归档）。
> 顶部先给出高层摘要；下文为细粒度展开。

## RULE

1. v1 不新训一套重型 segmenter 或全新 backbone，直接复用 MotionPatches 的 `14×5` patch grid，把创新集中到最终 structured score。
2. 训练和推理都保留 global retrieval 路径，但 structured path 必须真正参与最终排序，不能只做 auxiliary loss。
3. 样本按 `single / ordered / parallel` 三类处理，不强行用一个全序 matcher 吃掉所有 caption。

## 设计借鉴

- event 作为最小语义单元：[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]
- chronology negatives / shuffled order：[[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChroAccRet]]
- token-patch late interaction：[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]
- joint→segment→global 的层级对齐：[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]
- motion token 结构化分解：[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]

## 思路：

1. Data级：
   1. 每条 caption 先拆成 `event` 序列，并额外打上 `single / ordered / parallel` 标签；
   2. `ordered` 样本走有序匹配，`parallel` 样本走放宽顺序的匹配，`single` 样本直接保留 global fallback；
   3. 训练负样本优先构造 `shuffle / reverse / parallel->sequential` 三类，先解决“顺序错但语义接近”的 hard negative。
2. Pipeline级：
   1. Text side：`caption -> events -> event encoder`，输出每个 event 的语义向量；同时再预测一个 `body-group weight`，告诉模型这个 event 更该看腿、手臂还是躯干；
   2. Motion side：直接复用 MotionPatches 的 `14×5` patch tokens；沿时间维把每个 time bin 池化成 `14` 个 segment token，同时保留每个 segment 内的 `5` 个 body-group token；
   3. Matching side：先算 `event × segment × body-group` 相似度，再对 `ordered` 样本用 monotonic DP 求最优有序路径；对 `parallel` 样本取消局部顺序硬约束；对 `single` 样本退化为 global-global；
   4. Final score：`score = λ_g * global_score + λ_s * structured_score`，即先保留 baseline 的稳定语义检索，再用 structured score 修正时序和 body-part 误差。
3. Training policy级：
   1. `L_global` 保留当前 `S2E-v2` 的 global/event-aware 对比学习，保证 backbone 不崩；
   2. `L_order` 直接比较 `correct caption` 与 `shuffled caption` 的 structured score，逼模型学会“同词不同序”的区分；
   3. `L_struct` 让正确 motion-caption pair 的 structured score 大于跨样本 hard negatives；
   4. `L_group` 对 body-group weight 加轻量稀疏/熵约束，避免所有 event 都均匀看全身，失去可解释性。
4. Inference级：
   1. gallery 侧离线缓存 `global embedding + 14×5 patch tokens`，不引入额外 motion preprocessing；
   2. query 侧在线做 event decomposition，先用 global score 粗检索 top-K，再用 structured score rerank；
   3. 若 rerank 持续有效，再决定是否把 structured score 前移为主检索打分；v1 先走 coarse-to-fine，降低实现风险。

## 实验

1. `V1 Ordered Event-Segment Rerank`：
   1. 只做 `event encoder + segment pooling + monotonic DP score`；
   2. motion 侧只用现成 `14×5` tokens，不学新边界；
   3. 对比 `plain00 / S2E-v2`，看 `PrimaryScore + CAR/TAR` 是否同步提升。
2. `V2 Joint-Group Refinement`：
   1. 在 `V1` 基础上加入 `body-group weight`；
   2. 重点看 `left/right arm/leg`、`walk while wave`、`raise arm then squat` 这类局部/时序混淆样本；
   3. 验证 `temporal-only` 与 `temporal+group` 的差距，确认空间模块是不是必要组件。
3. `V3 Parallel-Aware Relaxation`：
   1. 只在检测到 `while / during / simultaneously / and` 并行 cue 的样本上开启 relaxed matching；
   2. 对比“全序 DP”与“parallel-aware”在并行动作子集上的收益；
   3. 若并行样本收益不明显，不把它升级成主创新。
4. Transfer / Ablation：
   1. `DistilBERT event encoder vs T5-base event encoder`；
   2. `rerank-only vs joint training`；
   3. `fixed 14-bin segment pooling vs soft event-position prior`。

## 一、Pivot 动机

### 1.1 旧路线天花板

- `stage5_s2e_v2` fair delta = +0.6212，normal retrieval 持平，delta 几乎全来自 97 条 nsim query
- 本质是"在全局 CLS 对齐框架里加 event-level contrastive loss"
- Rule_Insights Q1-Q3 论证：全局对齐上限已可见（MoCHA 正样本方差 11-19%，PST 证明细粒度可突破）
- 旧 S2E-v2 / REF00 结果降级为 pilot study / motivation

### 1.2 竞争格局空白

<!-- SECTION: competition_matrix -->

```
                    Spatial 粒度
                    Global            Joint/Part-level
Temporal   Global │ TMR, MoCHA       │ PST, MaxSim        │
粒度               │ (去噪/增强)       │ (金字塔/late-int)    │
           ───────┼──────────────────┼─────────────────────┤
           Event/ │ 旧 TAMR          │ ← 空白 ← 我们的位置   │
           Ordered│ (delta 太小)      │                     │
```

- PST：joint→segment→global 金字塔，但 segment 是空间压缩（KNN-DPC），permutation-invariant，无 temporal ordering
- MaxSim：joint-angle patch late interaction，text 侧仍是 word token，无 event structure
- Event-T2M：event decomposition + 时序条件化，但做 generation 不是 retrieval
- MoCHA：text denoising，仍是全局对齐
- FrankenMotion：part-level + temporal 标注，也是 generation
- PST / MaxSim 均闭源，作为同期工作讨论

右下角格子（temporal-ordered + spatial fine-grained retrieval）是空的。

## 二、核心方法：Event-Grounded Fine-Grained Matching

### 2.1 设计原则

- 时序感知是 primary axis（竞品最少，HumanML3D-E 已有 event annotation）
- 空间细粒度是 co-designed axis（从一开始就和时序模块联合设计）
- 两个轴通过统一的 structured matching score 融合

### 2.2 叙事定位

"event-grounded fine-grained motion-text matching"

<!-- SECTION: architecture -->

### 2.3 架构草案

```
Text side:
  "A person walks forward, then raises both arms"
      ▼ Event Decomposition (HumanML3D-E LLM annotation)
  [event_1: "walks forward"]  [event_2: "raises both arms"]
      ▼ Event Encoder (shared)
  e_1 ∈ R^D                   e_2 ∈ R^D
      ▼ Body-part attention hint
  e_1 → {legs: high, arms: low}   e_2 → {legs: low, arms: high}

Motion side:
  Joint features x_1..x_T  (T frames, J joints)
      ▼ Temporal Segmentation (learned or event-aligned)
  [seg_1: frames 1..k]  [seg_2: frames k+1..T]
      ▼ Segment Encoder (shared)
  s_1 ∈ R^{G×D}          s_2 ∈ R^{G×D}    (G = joint groups)

Matching:
  Ordered Event-Segment Matching:
    score = Σ_i sim(e_i, s_π(i)),  π order-preserving
  Joint-group refinement:
    sim(e_i, s_j) = Σ_g w_g(e_i) · cos(e_i^g, s_j^g)
  Per-joint variant (ablation):
    sim(e_i, s_j) = Σ_k w_k(e_i) · cos(e_i^k, s_j^k),  k ∈ 23 joints
```

### 2.4 与竞品差异化

| 维度        | PST                  | MaxSim      | MoCHA           | Ours                             |
| ----------- | -------------------- | ----------- | --------------- | -------------------------------- |
| Motion 粒度 | joint-segment-global | joint-patch | global          | temporal-segment × joint-group  |
| Text 粒度   | word token           | word token  | denoised global | event-level                      |
| 时序建模    | 无 (permutation-inv) | 无          | 无              | ordered matching                 |
| 空间建模    | joint-level 金字塔   | joint-angle | 无              | joint-group + per-joint ablation |

<!-- SECTION: spatial -->

### 2.5 为什么空间不能省

- "raises right arm" vs "raises left arm" 在纯 temporal segment level 无法区分
- PST / MaxSim 已证明 joint-level 对齐对区分此类 pair 至关重要
- 空间模块两级：joint-group（5-6 groups，优先）+ per-joint（23 joints，PRISM-inspired ablation）

## 三、可复用资产

直接复用：

- HumanML3D-E 数据集 + event decomposition + `HumanML3DEventDataset`
- Temporal negative generation infrastructure
- CAR/TAR/DIAG eval metrics + `humanml3de` strict split + eval pipeline
- MotionPatches backbone（motion encoder 起点）

降级为 pilot study：

- S2E-v2 / REF00 → "全局对齐 + temporal loss 的天花板" motivation

需要新建：

- Event-level text encoder
- Temporal segment encoder（with joint-group structure）
- Ordered event-segment matching module
- Event-segment alignment loss
- Fine-grained eval metrics（event grounding accuracy, temporal ordering accuracy）

## 四、Backbone 策略

先用 MotionPatches（已有 infra，PST 也用 MotionPatch 表示）。Month 2 视需要决定是否替换。

<!-- SECTION: timeline -->

## 五、执行 Timeline（ICLR 2027，~6 个月）

### Month 1 — Temporal-first prototype + hard gate

- Event text encoder + temporal segment encoder + ordered matching
- HumanML3D-E 上跑 temporal-only prototype
- Hard gate（见 §六）

### Month 2 — Spatial integration + ablation

- Joint-group spatial module，与 temporal module 联合训练
- Per-joint variant 实现
- 第一轮 ablation：temporal-only / spatial-only / temporal+spatial / joint-group vs per-joint
- 收集 PST / MaxSim / MoCHA 论文报告数值，构建 comparison table（同期工作）

### Month 3 — Method iteration + scaling

- 调整 loss balance、segment 策略
- Learned segmentation vs fixed window vs event-aligned
- KIT-ML 跨数据集实验

### Month 4 — Full ablation + analysis

- 完整 ablation table
- Event grounding 可视化 + temporal ordering accuracy
- Error analysis
### Month 5-6 — Paper writing + supplementary

- ICLR format draft
- Reviewer-anticipated experiments
- Camera-ready
## 六、Go/No-Go Gate（Month 1 末）

GO 条件（满足任一）：

- CAR@K / TAR 相对 global baseline（plain00 / TMR）有 >3pp 提升
- PrimaryScore 超过 plain00_s42 (43.83) 至少 +2.0

NO-GO 条件：

- PrimaryScore 低于 global baseline 且 CAR 无提升 → 重新评估方向

## 七、已确认决策

1. 旧 S2E-v2 降级为 pilot study / motivation — 已确认
2. PST / MaxSim 闭源 → 同期工作，论文报告数值做 comparison table
3. 叙事 → "event-grounded fine-grained motion-text matching"
4. Spatial → joint-group 优先 + per-joint ablation（PRISM-inspired）


## 八、方案评估与修订（2026-04-17）

### 原始思考

1. 对于 text 的 event decompose，是否需要从使用 HumanML3D-E-MP 改为使用 HY-Motion 的 rewrite 自己构建 HumanML3D-E、BABEL 等数据集的 decompose 增强？至少，需要先评估 HumanML3D-E-MP 的 decompose 是否合理（如并行动作是否被拆分为两个独立 event）
2. 动作数据增强，按照 [[Motion Data Rep|Motion Data Rep]]：修改数据表示，不用 guo263，改为 global position / kimodo 格式；joint 表示兼容 joint level 和 joint group
3. Text encoder 兼容：保留 DistilBERT，同时增加 T5 的兼容
4. Order-preserving matching 更新：担忧纯启发式规则的鲁棒性不足

### 评估 1：Event Decompose 质量

结论：**Month 1 不改，但需要做诊断**。

- 当前 HumanML3D-E 的 `data_{split}.npy` 中 100% caption 已有 `decomposed` 字段，格式可用
- 硬伤 (a)：50.7% caption 只有 K=1（单 event），提供不了时序分解信号
- 硬伤 (b)：decomposed event 没有 `f_tag/to_tag` 时间戳，temporal segment encoder 只能靠 fixed window
- 硬伤 (c)：并行动作（"while"/"during"）被扁平化为顺序列表，OrderedMatchingModule 无法区分

行动项：
1. Month 1 Week 1：跑 D0 诊断，统计 K>=2 样本中并行 cue 占比、event 长度分布
2. K>=2 且无并行 cue 样本 >= 30% 总量 → 足够支撑 temporal-only prototype
3. 不足 → Month 2 引入 HY-Motion rewrite 或 Gemini re-decompose，不阻塞 Month 1

### 评估 2：动作数据表示

结论：~~Month 1 保持 guo263~~ → **修正：Month 1 第一步优先做 motion 表示探索实验**。

修正原因（2026-04-17 补充）：
- MotionPatches baseline 使用 `new_joints/` (22×3 joint positions)，不是 guo263
- 后续所有模块（temporal segment encoder、matching、loss）都依赖固定的 motion 表示
- 如果先做 structured matching 再换表示，所有实验需要重跑
- 因此 motion 表示选型必须前置

数据溯源结论：
- 本地无原生 SMPL rotation（`amass_data/` 不存在），所有 rotation 均为 IK 重建
- guo263 的 rot_data 本身就是 IK 产物，因此 IK 重建的 rotation 表示和 guo263 精度等价
- `build_humanml3de_mp_motion_formats.py` 已实现 5 种 schema 的转换逻辑

行动项：
1. **Month 1 Week 1 前半**：跑 5 种表示的 baseline retrieval 对比实验（见 §九）
2. 选定表示后，固定 `motion_input_dim` 和 normalization stats，后续不再变动
3. Kimodo 格式不需要额外 SMPL 数据，因为 IK 精度和 guo263 等价

### 评估 3：Text Encoder 兼容

结论：**Month 1 保持 DistilBERT，Month 2 加 T5-base 作为 ablation**。

- `EventTextEncoder` 接收 `[N_evt, L', 768]` token embeddings，只需改 `input_dim` 即可适配
- T5 优势：encoder-decoder 架构对 event 级语义理解更强；[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 用 T5 做文本条件注入已有先例
- Month 1 核心假设是 "structured matching > global matching"，text encoder 不是瓶颈变量
- T5 版本选择：`t5-base`（768d，与 DistilBERT 同维度，最小改动）；更强语义用 `flan-t5-base`

行动项：
1. Month 1：DistilBERT 不动
2. Month 2：`EventTextEncoder` 加 `text_encoder_type` 参数，支持 `{"distilbert", "t5-base", "flan-t5-base"}`
3. T5 token embedding 提取需新 preprocessing pipeline，列为 Month 2 数据准备任务

### 评估 4：Order-Preserving Matching 鲁棒性

结论：**担忧合理，但当前 DP matching 已是 soft 版本，不依赖硬规则**。

- `OrderedMatchingModule` 用 DP 最优分配（`max Σ sim(e_i, s_π(i))` 且 π 保序），本身就是 soft matching——event 顺序和 segment 顺序不完全对齐时，DP 会找最优 partial alignment
- 真正的鲁棒性风险：(a) 并行 event 被强制排序；(b) K=1 样本退化为 "选最相似 segment"，和 global matching 无本质区别
- 解决方案不是放弃 order-preserving，而是分层处理

行动项：
1. Month 1：保持 DP matching，但在 loss 中对 K=1 样本加 global fallback（segment mean → global contrastive）
2. Month 2：引入 `parallel_event_mask [B, E]`，并行 event 之间不强制顺序约束
3. Month 3：如果并行 cue 占比 > 15%，考虑升级为 DAG matching（partial order）

### 修订后的 Month 1 执行计划

原计划调整，motion 表示探索前置：

1. **Step 0：Motion 表示探索**（Week 1 前半）
   - 用 `build_humanml3de_mp_motion_formats.py` 导出 5 种表示
   - 用 MotionPatches 的 global contrastive baseline 跑 5 种表示的 retrieval 对比
   - 选定最优表示，固定 `motion_input_dim` 和 normalization stats
   - 详见 §九
2. **Step 1：D0 诊断**（Week 1 后半）：统计 decompose 质量，确认 K>=2 无并行 cue 样本量
3. **Step 2：Structured matching prototype**（Week 2-3）：基于选定表示实现 temporal-first prototype
4. **K=1 global fallback**：在 `EventGroundedContrastiveLoss` 中加入 K=1 样本的 global contrastive 分支
5. **Go/No-Go gate 不变**：CAR@K > +3pp 或 PrimaryScore > 45.83

## 九、Motion 表示探索实验设计（Step 0）

### 9.1 目标

在 structured matching 之前，用最简单的 global contrastive baseline 对比 5 种 motion 表示，选出最优表示后固定。

### 9.2 候选表示

| Schema | 维度 | 内容 | 数据来源 |
|--------|------|------|----------|
| `guo263` | 263 | root(4) + ric_pos(63) + rot_6d(126) + vel(66) + foot(4) | `new_joint_vecs/` 直接可用 |
| `pos66` | 66 | 22 joints × 3D global position | `new_joints/` 直接可用（MotionPatches baseline） |
| `smpl_d135_recon` | 135 | root(6) + 21 joints × 6D cont rotation + foot(3) | IK 重建，精度等同 guo263 rot |
| `hy201_recon` | 201 | root(6) + pos(63) + rot_6d(126) + foot(6) | IK 重建，pos+rot 混合 |
| `kimodo_like_261` | 261 | root(6) + heading(1) + pos(63) + vel(63) + rot_6d(126) + foot(2) | IK 重建，最丰富 |

### 9.3 实验设计

控制变量：只改 motion 表示，其他全部固定。

- Motion encoder：轻量 Transformer（2 层，D=256），和 `TemporalSegmentEncoder` 内部的 segment encoder 同架构，但输出 global embedding（mean pool over T）
- Text encoder：DistilBERT token embeddings → 同架构 Transformer → global embedding
- Loss：标准 symmetric InfoNCE，τ=0.07
- 数据：HumanML3D-E-MP，train/val/test split 不变
- 评估：R@1, R@5, R@10, MedR（t2m + m2t），PrimaryScore

每种表示需要：
1. 导出 motion 数据（`build_humanml3de_mp_motion_formats.py`）
2. 计算 Mean/Std normalization stats
3. 训练 global contrastive baseline（~50 epochs，early stop on val R@1）
4. 在 test set 上评估

### 9.4 预期产出

- 5 种表示的 retrieval 指标对比表
- 选定表示的 `motion_input_dim`、`Mean.npy`、`Std.npy`
- 如果 `pos66` 和最优表示差距 < 1pp，优先选 `pos66`（和 MotionPatches baseline 对齐，减少变量）

### 9.5 所需代码

1. `scripts/build_motion_format_stats.py`：对每种 schema 计算 Mean/Std
2. `scripts/run_motion_repr_ablation.py`：自动化 5 种表示的训练+评估 pipeline
3. `src/data/motion_repr_dataset.py`：支持多种 motion 表示的 Dataset 类
4. `configs/experiment/motion_repr_ablation.yaml`：Hydra config
