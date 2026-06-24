---
updated: 2026-04-11
created: 1970-01-01T08:00
status: historical
note: >
  v3 高层 roadmap。Phase 划分和 backbone 迁移计划以
  2026-04-11_tamr-roadmap-phase1-vs-phase2.md 为准。
  Stage4.1 执行细节以 V4 narrow-scope 为准。
---
## created: 2026-04-06

updated: 2026-04-11T10:30
source:

- paperIDEAs/TAMR/2026-04-05_tamr-motionpatches-harness-design.md
- paperIDEAs/TAMR/eval_summary/2026-04-06_tamr-motionpatches-stage1-closure-summary.md
- paperIDEAs/TAMR/eval_summary/2026-04-09_tamr-motionpatches-stage2-closure-summary.md
- paperIDEAs/TAMR/eval_summary/2026-04-10_tamr-motionpatches-stage4-first-pass-eval-summary.md
- paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches.md
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/scripts/train.py
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/scripts/test.py
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/temporal_utils.py
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/models/clip.py
tags:
- research-idea
- TAMR
- temporal-aware
- motion-text-retrieval
- motionpatches
- event-abstraction
- coarse-grounding
- execution-roadmap
status: execution-roadmap
title: "TAMR v3: Event-Abstraction-Centered Stepwise Roadmap"
model_name: TAMR

# TAMR v3: Event-Abstraction-Centered Stepwise Roadmap

> 本文保留为 TAMR 的高层 stepwise roadmap。
> 自 `2026-04-10` 的 Stage4.1 收缩后，具体执行以 `Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v4-narrow-scope-execution.md` 为准。
> Stage4.1 的历史收敛与已清理旧稿见 `Temporal_Alignment/2026-04-10_temporal-alignment-scheme-evolution.md`。
> `2026-04-11` 的最新执行结果见 `Temporal_Alignment/2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md`。

本文不再承担 Stage4.1 的逐版机制设计记录；它负责保留整个 TAMR 的阶段切分、主线约束和执行顺序。

其目标不是把 MotionPatches 扩展成重型 grounding 系统，而是以事件抽象为核心，把强语义检索推进为面向时序理解的 retrieval-centered framework。

当前正式口径固定为：

1. backbone 使用 MotionPatches
2. 正式监督基础使用 HumanML3D-E 的 GT `decomposed` event text
3. 当前动作输入保持整段 motion，不先切成 motion clips
4. temporal evidence 只做 coarse supporting evidence，不做 dense grounding
5. 所有后续修改都以“先固定评测与回归支架，再扩展模型”为原则推进

## 0. Setting and Terminology Quick Map

先把当前会反复出现的几个 setting 固定下来：


| Setting                       | MotionPatches 状态        | event 来源                                                  | 是否切 motion | 概念解释                                                                        |
| ----------------------------- | ----------------------- | --------------------------------------------------------- | ---------- | --------------------------------------------------------------------------- |
| `baseline`                    | 原始全局检索路径                | 无 event decomposition，直接使用整句 caption                      | 否          | 这是原生 MotionPatches 对照组，不启用 event-aware / temporal-aware scaffold。           |
| `rule`                        | 启用 event-aware scaffold | `temporal_utils.py::split_caption_into_events()` 的启发式文本切分 | 否          | 这是“heuristic event split”对应的实验 setting，本质上是规则/正则驱动的文本侧 event decomposition。 |
| `HumanML3D-E gt event` / `gt` | 启用 event-aware scaffold | HumanML3D-E `data_<split>.npy` 里的 GT `decomposed` events  | 否          | 这是当前 TAMR v3 的正式主线 setting，用人工整理好的事件分解替换规则切分。                               |
| `gt_fallback_rule`            | 启用 event-aware scaffold | 优先 GT，缺失时退回 rule                                          | 否          | 这是工程兜底 setting，可用于过渡或容错，但不是当前最推荐的论文主线。                                      |


这里还需要额外固定两个术语：

1. 文中说的 **heuristic event split / heuristic split**，在当前 `MotionPatches-main` 代码语境里，就是 **rule-based split**。
2. 这个 split 指的是 **文本侧 caption -> events 的切分**，不是 **动作侧 motion segmentation**。

术语更正：

- 下文不再使用 `harness` 指代这些评测、诊断、回归产物，以免和 agent harness / 权限边界设定混淆。
- 相关术语统一改为：**评测与回归支架**、**诊断视图**、**能力层级（`H0-H4`）**。

## 1. 核心定位

TAMR 的主任务是 temporal discriminative retrieval。

它要解决的问题不是“语义检索还能不能多涨一点 R@1”，而是：

1. 模型能否理解 caption 中的事件顺序与时间关系
2. 这种能力能否在检索表示层被稳定注入
3. 模型能否输出粗粒度时间证据，证明自己不是只在做全局语义匹配

因此当前任务层次固定为：

1. **主任务**：temporal discriminative retrieval
2. **辅助证据**：coarse temporal evidence
3. **不纳入当前主线**：开放式问答、统一 understanding 平台、dense grounding

## 2. Event Abstraction 的正式含义

这里的 event abstraction，指的是把原始 caption 从整句全局描述提升为可用于检索训练的事件结构。

它至少包含三层信息：

1. **事件列表**
  - 例如把 `raise both arms and then squat` 拆成有序事件序列
2. **事件顺序**
  - 明确 `event 0 -> event 1`
3. **事件关系**
  - 例如 before / after / while / duration / negation / count

当前版本中，event abstraction 首先发生在**文本侧**，不是先做动作切段。

## 3. 当前固定不变的主线约束

后续所有评测与回归支架相关改动，都先以以下约束为准：

1. **保留 MotionPatches 原始全局检索路径**
2. **先验证 GT event text 是否带来稳定时序增益**
3. **先扩展评测、诊断与回归输出，再扩展模型结构**
4. **先保持整段 motion 输入，再考虑更细粒度 motion-side temporal modeling**
5. **新增模块必须可以回到 baseline 做严格对比**

### 3.1 当前进度总览（2026-04-10）


| Step   | 当前状态 | Train | Eval | Summary | 当前判断 | 下一步 |
| ------ | ------ | ----- | ---- | ------- | ------- | ------ |
| Step 0 | 已完成 | - | 已完成 | 已完成 | baseline 与评测/回归约束已锁定 | 无 |
| Step 1 | 已完成 | 已完成 | 已完成 | 已完成 | GT event 路径已打通，temporal gain 明确，标准 retrieval 仍有 trade-off | 保持 `event_source.type=gt` 为主线 |
| Step 2 | 已完成（aggregate level） | 已完成 | 已完成 | 已完成 | `HumanML3D-E-only` GT event 主线已经证明自己有效 | 已进入后续阶段 |
| Step 3 | 已完成（diagnostic view） | - | 已完成 | 已完成 | `test.py + temporal_utils.py` 已稳定导出 `DIAG_ordering/before/after/negation/duration/existence`，并完成 `stage2_mp_gt_step3diag` 全量回归 | 作为 Step 4 的固定验收面板 |
| Step 4 | 首轮闭环已完成（未通过） | 已完成 | 已完成 | 已完成 | token-level temporal adapter 首轮在 `nsim` hard temporal slice 出现系统性退化，未满足 go/no-go | 进入 Step 4.1 问题定位与轻量迭代 |
| Step 5 | 未开始（阻塞） | 未开始 | 未开始 | 未开始 | Step 4 未过 gate，当前不应前置 | 等 Step 4 通过后再进 |


当前 roadmap 的实际执行含义应理解为：

1. **Step 0-3 已经闭环，且 Step 3 诊断视图成为固定验收入口**
2. **Step 4 首轮结论为 no-go，当前不进入 Step 5**
3. **后续实验继续固定沿 `HumanML3D-E` GT event 主线推进**
4. **下一步优先做 Step 4.1（adapter 轻量消融与稳定性修复），而不是继续加重模型**

## 4. Step Roadmap

### Step 0: Freeze Baseline and Eval/Regression Contract

目标：

- 固定 MotionPatches baseline
- 固定 strict TMR-aligned fair comparison
- 固定 temporal eval 与 generation proxy 的输出口径

主要改动位置：

- `MotionPatches-main/scripts/train.py`
- `MotionPatches-main/scripts/test.py`
- `MotionPatches-main/conf/config.yaml`
- `MotionPatches-main/conf/test_config.yaml`

本步不做什么：

- 不新增 event-aware architecture
- 不改 motion encoder 结构
- 不改 checkpoint 命名口径

go / no-go：

- baseline 指标稳定可复现
- eval 输出路径稳定
- 后续所有改动都能回到这个基线比较

对应能力层级：

- `H0`

当前状态（2026-04-09）：

- 已完成。
- baseline、strict fair retrieval、temporal eval、generation proxy 的输出路径都已固定。

### Step 1: Replace Heuristic Event Split with HumanML3D-E GT Events

目标：

- 用 HumanML3D-E 的 GT `decomposed` event text 替换启发式事件切分
- 保持 motion 侧仍为整段输入
- 先验证真实事件文本监督本身是否有帮助

主要改动位置：

- `MotionPatches-main/temporal_utils.py`
- `MotionPatches-main/scripts/train.py`
- `MotionPatches-main/scripts/test.py`

推荐最小实现：

- 默认 `event_source.type=gt`
- train / val / test 都按 HumanML3D-E 对应 split 读取 GT events
- 不暴露 motion token-level 表征

go / no-go：

- temporal retrieval 相比 baseline 有清晰增益
- 标准 retrieval 不出现灾难性退化
- GT 事件监督路径可稳定复用到训练和评测

对应能力层级：

- `H1`
- `H2`

当前状态（2026-04-09）：

- 已完成。
- GT event source 已经稳定打通训练与评测。
- 当前剩余问题不再是“GT 路径是否可用”，而是“GT 路径在不同 protocol 上的收益如何诊断与稳定”。

### Step 2: Run HumanML3D-E-Only Event-Aware Retrieval

目标：

- 在 HumanML3D-E-only 主线下把 event-aware retrieval 跑稳
- 增加 relation-sensitive temporal negatives
- 建立“event abstraction 本身有效”的独立证据

主要改动位置：

- `MotionPatches-main/temporal_utils.py`
- `MotionPatches-main/scripts/train.py`
- `MotionPatches-main/scripts/test.py`
- `MotionPatches-main/models/clip.py`

推荐最小实现：

- 保留当前 global embedding 路径
- event loss 与 temporal hard negative loss 继续基于文本侧结构构造
- before / after / ordering / negation / duration 先从文本侧 relation-aware negatives 起步

本步仍不做什么：

- 不暴露 motion token-level features
- 不做 evidence head
- 不引入新的动作侧时间监督分支

go / no-go：

- `CAR@K`、`TAR@K` 有稳定提升
- temporal gain 能在 `HumanML3D-E-only` 设定下成立
- 能明确说明增益来自 event abstraction，而不是来自额外复杂结构

对应能力层级：

- `H2`
- `H3`

当前状态（2026-04-09）：

- 已完成 aggregate-level 的 train / eval / summary。
- 当前证据已经表明：仅靠 `HumanML3D-E` GT events 也能得到稳定 temporal gain。
- 但现有输出仍主要是聚合 `CAR/TAR`，还不足以直接替代 Step 3 的 capability diagnosis。

### Step 3: Expand Diagnostic Views Before Expanding Architecture

目标：

- 先把诊断切片与评测面板补完整
- 明确每种提升到底来自哪类 temporal capability
- 在模型仍然轻量时先完成能力诊断

主要改动位置：

- `MotionPatches-main/scripts/test.py`
- `MotionPatches-main/temporal_utils.py`
- 如有需要，再补 dataset / metrics export 脚本

优先补齐的诊断视图：

- ordering
- before / after
- existence
- negation
- duration-sensitive variation
go / no-go：

- 至少能把 `H1/H2/H3` 的能力边界分开报告
- 能清楚区分“标准语义检索变好”与“temporal following 变好”
- regression 输出已经足够支撑后续架构改动

对应能力层级：

- `H1`
- `H2`
- `H3`

当前状态（2026-04-10）：

- Step 3 已完成闭环并固化为回归面板：
  - `MotionPatches-main/temporal_utils.py` 已导出 `diagnostic_negative_texts` 与 `diagnostic_dimensions`，覆盖 `ordering / before / after / negation / duration / existence`；
  - `MotionPatches-main/scripts/test.py` 的 `compute_temporal_metrics()` 已稳定输出 `t2m/DIAG_*`（queries、`R@K`、margin）并保留 `CAR/TAR`。
- 已完成 full eval 导出（GT 主线）：
  - `checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/EVT-normal.yaml`
  - `checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
- Step 4 的首轮评测已直接复用该诊断面板，验证了 Step 3 的可复用性与稳定性。

### Step 4: Expose Token-Level Motion Features and Add a Temporal Adapter

目标：

- 在 Step 2 和 Step 3 已稳定后，再把 motion-side temporal modeling 接出来
- 暴露 MotionPatches 的 token-level motion features
- 在 token-level features 上增加轻量 temporal adapter

主要改动位置：

- `MotionPatches-main/models/clip.py`
- `MotionPatches-main/scripts/train.py`
- `MotionPatches-main/scripts/test.py`

推荐最小实现：

- 保留原始 global retrieval 路径
- 新增 token-level temporal branch，但不破坏 baseline 对比口径
- temporal adapter 先轻量，不上重型 grounding machinery

go / no-go：

- token-level temporal branch 带来稳定 temporal gain
- 标准 retrieval 没有被明显伤害
- 该模块的收益能与纯文本侧 event abstraction 区分开

对应能力层级：

- `H3`

当前状态（2026-04-10）：

- 已完成首轮 stage4 train + full eval + summary：
  - run：`checkpoints/stage4_mp_gt_adapter/HumanML3D`
  - eval（inf ON）：`checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/`
  - 诊断消融（同 checkpoint，`eval.temporal_adapter.use_inference=false`）：
    - `checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/`
- 首轮结果未通过 go/no-go（No-Go）：
  - `TMR-nsim t2m/R01: 57.00 -> 46.00`（相对 stage2，`-11`）
  - `EVT-nsim CAR01: 66.67 -> 56.25`，`TAR01: 33.00 -> 23.00`
  - 诊断维度在 `EVT-nsim` 上出现系统性回撤（`ordering/before/after/negation/duration/existence` 全线下降）。
- 诊断结论：
  - 关闭 adapter 推理分支可部分恢复 `nsim`（例如 `EVT-nsim CAR01 +4.17`），但仍明显低于 stage2；
  - 说明问题同时存在于 inference path 与 training phase 表示漂移；
  - 当前不应进入 Step 5，应先进入 Step 4.1 轻量修复迭代。
- Stage4.1 的当前具体路径已固定为 `D0 -> D1 -> D1.5 -> D2 -> D3` narrow-scope plan，详见 `Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v4-narrow-scope-execution.md`。
- `2026-04-11` 的 `D0` 已执行并判定 `GO`；当前 blocker 已前移到 `D1` 的 frozen minimal event-time head。

### Step 5: Add Coarse Evidence Head

目标：

- 在已有 temporal gain 的基础上，再增加 coarse temporal evidence 输出
- 回答“该事件是否存在”以及“它大概出现在什么时候”

主要改动位置：

- `MotionPatches-main/models/clip.py`
- `MotionPatches-main/scripts/train.py`
- `MotionPatches-main/scripts/test.py`

推荐最小实现：

- existence logit
- `start_bin / end_bin` 或 coarse bin distribution
- 输出仅服务于 retrieval-centered evidence，不扩展成 dense grounding

前提：

- Step 4 已经能稳定暴露 token-level features

go / no-go：

- existence 指标优于简单阈值法
- coarse span hit / bin overlap 具有解释性
- 可以用案例证明模型不只是做全局语义匹配

对应能力层级：

- `H4`

当前状态（2026-04-10）：

- 尚未开始（阻塞）。
- Step 4 首轮未通过 gate，当前继续阻塞 Step 5。

## 5. 代码修改优先顺序

如果后续按最小成本继续改评测与回归支架，建议严格按下面顺序推进：

1. `scripts/test.py`
  - 先让评测面板和 regression 输出稳定
2. `temporal_utils.py`
  - 再固化 GT events、temporal negatives、诊断视图的 data contract
3. `scripts/train.py`
  - 然后把训练逻辑绑定到已固定的数据 contract 与评测口径
4. `models/clip.py`
  - 最后才做 token-level temporal branch 与 evidence head

这个顺序的核心原因是：

> 先把“如何验证”固定，再扩展“如何建模”，这样后续每一步时序增量都能被明确归因。

## 6. 当前一句话执行口径

> TAMR 当前已完成 Step 0-3 闭环并确认 Step 4 首轮 `No-Go`；Stage4.1 的实际执行路径固定为 `D0 -> D1 -> D1.5 -> D2 -> D3`，其中 `D0` 已在 `2026-04-11` 给出 `GO`，因此下一步应进入 `D1` 的 frozen minimal event-time head，而不是回到 full `BASMA+` 或前置 Step 5。
