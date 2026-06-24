# TAMR Experiments

## 读取规则

- 只承认 same-family 对照。
- TMR / ACTOR 和 MotionPatches 只做机制迁移，不做分数横比。
- `REF00` 是 rerun，不是新方法。

## 1. TMR 机制探针


| 实验     | 对照      | 关键改动                                   | 关键结果                                                                                    | 判定                        |
| ------ | ------- | -------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------- |
| `D0`   | 数据 gate | 只检查 event 分解是否足够支撑最小探针                 | `K>=2 = 70.58%`，overlap 规则占比 `4.48%`                                                    | 可以进入 `D1`                 |
| `D1`   | `T-B0`  | 最小 event-time head，backbone 全冻结        | `val_evt_align_acc` best `0.3960`；retrieval 基本不变                                        | frozen feature 里有可提取时序信号  |
| `D1.5` | `D1`    | `attention pooling -> uniform pooling` | `val_evt_align_acc` best `0.1677`，比 `D1` 低 `22.82pp`；retrieval 完全相同                     | attention 必须保留            |
| `D2a`  | `D1`    | 只解冻最后 2 个 motion block                 | normal `t2m R@1 9.46 -> 13.51`，`m2t R@1 2.70 -> 16.22`；nsim `13 -> 17`，`3 -> 26`        | controlled unfreeze 安全且有效 |
| `D2b`  | `D2a`   | 解冻整个 motion encoder                    | normal `13.51 -> 15.54`，`16.22 -> 22.30`；nsim `17 -> 22`，`26 -> 33`；best align `0.4332` | Stage4.1 winner           |


补充保留：

- 后续更大口径笔记里，full corrected corpus 仍提示 `K=1` 样本占比很高，说明 temporal supervision density 先天有限。

## 2. MotionPatches 主线

### 当前 fair scoreboard


| 运行                   | 机制                                               | PrimaryScore | 相对 `plain00_s42` | 判定                   |
| -------------------- | ------------------------------------------------ | ------------ | ---------------- | -------------------- |
| `plain00_s42`        | 纯 global baseline                                | `43.8275`    | `0`              | 当前 fair anchor       |
| `stage5_s2e_v2` fair | `event CLIP + temporal negatives`，最终仍是 global 打分 | `44.4487`    | `+0.6212`        | 当前最强 same-regime 正信号 |
| `ref00_s42` fair     | `S2E-v2` family rerun                            | `43.8662`    | `+0.0387`        | rerun reference only |


### 必须保留的负结果


| 实验                 | 对照                   | 关键结果                                                  | 判定                       |
| ------------------ | -------------------- | ----------------------------------------------------- | ------------------------ |
| `MP heavy adapter` | `stage2_gt`          | `TMR-nsim t2m R@1 57 -> 46`；`EVT-nsim TAR@1 33 -> 23` | 重型 temporal adapter 直接停用 |
| `S2E+T` legacy     | `S2E-v2` legacy eval | `43.97 < 44.50`                                       | 只加 temporal head 没解决核心瓶颈 |


### `REF00` 的唯一合法定位

- fair re-eval 只比 `plain00_s42` 高 `+0.0387`，不能当当前 baseline。
- 旧 `44.7481 ± 0.7944` 来自 legacy gallery root，只能当 seed 方差参考。

## 3. Motion representation 前置实验（⚠️ 已降低优先级，等 R1 验证后再决定是否继续扩线）

### 3.1 Vanilla TMR / HumanML3D-E-MP 6-way fair eval

> setting: 同一 `vanilla TMR + HumanML3D-E-MP + DistilBERT + 500ep`，仅替换 motion data source / adapter。same-dataset internal baseline 为 `guo263`。

| Rank | Schema | PrimaryScore | 相对 `guo263` | 关键结果 | 判定 |
| ---- | ---- | ----: | ----: | ---- | ---- |
| 1 | `kimodo261` | `40.58` | `+4.09` | `normal t2m/R@1=5.57`，`nsim t2m/R@1=50.52`，`guo t2m/R@1=65.06` | clear winner |
| 2 | `pos66` | `37.45` | `+0.96` | `nsim t2m/R@1=48.45`，最接近 MP 原生表示 | second tier |
| 3 | `hml272` | `37.38` | `+0.89` | 整体均衡，但无单项第一 | second tier |
| 4 | `hy201` | `37.35` | `+0.86` | `normal m2t/R@1=8.85` 全部 run 第一 | second tier |
| 5 | `guo263` | `36.49` | `0` | 内部 baseline，不再是最优 | baseline only |
| 6 | `smpl135` | `3.86` | `-32.63` | `normal t2m/R@1=0.09`，local rerun 出现 tiny-std warning | collapse / 排除 |

保留结论：

- 在 vanilla TMR 这条线里，`kimodo261` 是唯一显著领先的 motion rep。
- `pos66 / hml272 / hy201` 是非常接近的第二梯队，彼此差距小于 `0.11` PrimaryScore。
- `guo263` 不能再单独代表 same-family baseline。
- `smpl135` 当前更像 representation / normalization 异常，而不是正常弱基线。
- 这组结果完成了 TMR 侧 motion rep sanity check，但**不自动推翻** MotionPatches R1 继续使用 `pos66 + DistilBERT` 的最小变量决策。

### 3.2 Earlier lightweight MotionReprBaseline result（⚠️ 非 vanilla TMR，也非 MP 原生架构）

> ⚠️ **Setting 说明（非 MotionPatches 原生架构）**：以下实验基于 `MotionReprBaseline`（2 层轻量 Transformer，D=256，冻结 text encoder），checkpoint 约 9MB，**不包含** MotionPatches 的 ViT-B/16 主干权重。结论不可直接迁移到 MotionPatches `ClipModel` 框架。Phase 0.5（在完整 ClipModel 下的公平消融）已降低优先级，相关 prompt 见 `archived/motion_repr_text_encoder/phase0.5_motion_repr_clipmodel.md`。

| Rank | Schema            | PrimaryScore | 结论            |
| ---- | ----------------- | ------------ | ------------- |
| 1    | `kimodo_like_261` | `14.16`      | 单次最优          |
| 2    | `pos66`           | `14.05`      | 与第一名只差 `0.11` |
| 3    | `guo263`          | `13.37`      | 不占优           |
| 4    | `hy201_recon`     | `13.03`      | 不占优           |
| 5    | `smpl_d135_recon` | `11.84`      | 明显最差          |


当前只保留一个结论：

- 早期轻量 baseline 里，motion representation 会影响底线，但 `0.11` 的单次差距解释不了 TAMR 主线停滞；它不是当前核心矛盾。

### Text encoder probe on motion-repr baseline

> ⚠️ **Setting 说明（非 MotionPatches 原生架构）**：同上，基于 `MotionReprBaseline` 9MB checkpoint，text encoder 收益是 schema-dependent，不可直接迁移。

只记录 same-family 的局部结论。以下均以 **rerun test metrics** 为准：

| Schema | Text encoder | PrimaryScore | 相对 DistilBERT | 结论 |
| ---- | ---- | ----: | ----: | ---- |
| `kimodo_like_261` | `distilbert-base-uncased` | `13.62` | `0` | rerun baseline |
| `kimodo_like_261` | `flan-t5-base` | `14.15` | `+0.53` | 有稳定增益 |
| `kimodo_like_261` | `t5-base` | `14.84` | `+1.22` | 当前最优 |
| `kimodo_like_261` | `t5-large` | `13.79` | `+0.17` | 只剩弱增益 |
| `pos66` | `distilbert-base-uncased` | `14.02` | `0` | rerun baseline |
| `pos66` | `flan-t5-base` | `13.36` | `-0.66` | 明显退化 |
| `pos66` | `t5-base` | `13.47` | `-0.55` | 明显退化 |
| `pos66` | `t5-large` | `14.09` | `+0.07` | 几乎持平 |

补充保留：

- text encoder 的收益是 **schema-dependent**，不是无条件正向。
- `kimodo_like_261 + t5-base` 仍是当前 text-side 最优，但 rerun 后收益收缩到 `+1.22`。
- `pos66` 对 text encoder 基本不敏感；`t5-large` 也只比 DistilBERT 高 `+0.07`。
- auto-saved `metrics.json` 和 rerun test 指标存在系统差异，主要出现在 `m2t` 侧；后续应以 rerun 结果为准。
- 这些 checkpoint 都只有约 `9MB`，这是正常的：`best_model.pt` 只保存轻量 `MotionReprBaseline` 的 `state_dict`，不包含外部 Hugging Face text encoder 权重，也不包含 MotionPatches 主干 ViT。

## 4. 最终保留结论

- 真正有效的 TMR 机制信号是 `minimal head + unfreeze`，不是 heavy branch。
- MotionPatches 当前最强结果仍然属于 global event-aware 训练，而不是结构化 matching。
- `REF00` 只能做 variance audit，不能再驱动 roadmap。
- 下一步若不改最终 retrieval score，本项目只会继续得到小幅 smoke gain。

## 5. 已删除内容的处理原则

- phase / hybrid / pivot / architecture QA / prompt / temporal 草稿已并入本文件和 `ROADMAP.md`。
- 被删内容里只有机制结论和有效数值被保留；重复叙事、旧口径、过时 gate 已全部移除。
