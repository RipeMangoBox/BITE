---
title: "StoryMotion v8.3 Data Curation Preregistration"
status: preregistered_blocked_no_promoted_representation
workflow_state: not_started
gate: promoted_representation_selection
gate_state: closed
processed_pairs: 0
annotated_pairs: 0
quarantined_pairs: 0
materialized_manifests: 0
launched_jobs: 0
hypothesis: |
  在冻结同一 Stage1 representation、owning decoder 与 Unified Stage2 backbone 后，仅用可追溯的物理异常和 caption-motion pair 级语义错配 quarantine 替换 raw train manifest，可能改善生成动作的物理与文本一致性；该假设必须通过 raw-vs-clean 单变量实验验证，不能与 representation 或 generator 改动合并归因。
tags:
  - StoryMotion
  - v8
  - data-curation
  - preregistration
  - status/waiting
aliases:
  - StoryMotion-v8.3-Curation-Plan
source_notes:
  - "[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]"
created: 2026-07-17T17:35:00+08:00
updated: 2026-07-18T15:20:00+08:00
---

# StoryMotion v8.3 Data Curation Preregistration

> [!warning] 当前执行状态
> 本文是 v8.3 的唯一 plan 与 progress owner。v8.1A、v8.1B 与 v8.2 的 Stage1 endpoint 已完成，但没有 representation 通过原始 promotion gate；因此 `promoted_representation_selection` 保持 `closed`。尚未扫描、打分、标注、quarantine、物化 manifest 或启动 raw-vs-clean 训练。

## 0. 当前执行状态

| 字段 | 值 |
| --- | --- |
| recorded at | `2026-07-18 15:20 CST` |
| execution gate | `promoted_representation_selection` |
| gate state | `closed` |
| workflow state | `not_started / blocked_no_promoted_representation` |
| processed or scored pairs | `0` |
| manually annotated pairs | `0 / 300–500` |
| quarantined pairs | `0` |
| materialized manifests | `0 / 4` |
| scorer jobs launched | `0` |
| GPU jobs launched | `0` |

这些 `0` 表示从未开始，不表示扫描后未发现问题。v8.1A 的 amended non-promotion screen 不构成 v8.3 的 representation selection；在新的 prospective promotion 决定出现前，raw parent 继续是唯一有效数据源。

## 1. 问题、数据边界与因果边界

- **目标**：判断经过人工校准的物理异常与 pair-level 语义错配 quarantine，能否在固定 representation/backbone 下改善 StoryMotion 的 human、camera 与 joint 生成质量。
- **源数据**：完整 ordered `162,760` train IDs 对应的 Pulp raw train manifest 及 caption 展开后的 pair 集合。实际 motion 数、caption 数和 pair 数必须在启动后从 raw parent 审计得到，不在本计划中臆造。
- **选择规则**：先对完整 raw train parent 建只读快照；物理规则作用于 motion 证据但输出可逆的受影响 pair 记录，语义规则只作用于 `(motion_id, caption_id)`。test/eval 不参与阈值拟合。
- **人工预算**：目标 `400` 个分层 pair，允许范围 `300–500`；少于 `300` 不冻结阈值，超过 `500` 需另行授权。
- **输出目标**：四层 immutable manifest、校准标签与 scorer/threshold provenance、manifest lineage/audit，以及后续 matched raw-vs-clean Stage2 run contracts。

v8.3 是独立的 **data-curation axis**，不是 v8.2 representation 的一部分，也不是新的 Stage2 backbone。首个可归因实验固定已经选定的 Stage1 checkpoint、owning decoder、latent cache contract 和 Unified Stage2 实现，只改变 train manifest。不得同时更换 human feature layout、Stage1 checkpoint family、denoiser、task routing、sampler 或评测集。

数据清洗主要检验 Stage2 prior，不回溯解释 v7.14/v8.2 的 Stage1 reconstruction。若将来要检验 clean data 对 Stage1 的作用，必须另建 Stage1 raw-vs-clean run family；不得与本计划的 Stage2 结果合并成一个“clean system”结论。

## 2. 启动 gate

按顺序满足以下 gate 后才能前进：

1. **G0 — promoted representation selection**：Stage1 endpoint 的 completion marker、checkpoint、owning decoder 与 SHA256 可核验，且有一条 representation 通过其 prospective promotion gate 并被明确选择。当前三条 v8 endpoint 均未满足该条件，故不得启动 v8.3。
2. **G1 — raw parent lock**：记录原始 manifest path/SHA256、ordered ID SHA256、split、motion/caption/pair counts 和 source revision；raw snapshot 写成新 immutable artifact，不修改 parent。
3. **G2 — scorer availability**：TMR 与 LaMP 的代码版本、预处理版本、checkpoint path 和 SHA256 全部核验；PST 只有在可复现 checkpoint 与 hash 到位后才允许启用。
4. **G3 — calibration**：完成 `300–500` 个分层 pair 的人工标签，冻结 reason-code、physical rule 和 semantic threshold 版本。
5. **G4 — manifest audit**：四层 manifest 通过 membership、order、hash、lineage、scope 和 set-equation 检查。
6. **G5 — ablation contract**：raw 与 clean 两个 Stage2 run 的所有非数据字段逐项相等后，才能训练。

任何 gate 失败都保持 raw parent 为有效数据源；不得把部分产物命名为 clean endpoint。

## 3. 四层 immutable manifest

四层文件都采用 JSONL data 加 JSON metadata sidecar。写出后只读；规则、阈值或标签变化必须产生新 revision 和新 hash，禁止覆盖旧文件。

| manifest | 内容 | parent 与顺序规则 |
| --- | --- | --- |
| `raw` | source train manifest 的完整 pair-level snapshot | metadata 记录 source path/hash；保持原始 ordered motion IDs 与 caption order |
| `physical_quarantine` | 被高置信物理规则命中的 pair；同一坏 motion 的每个受影响 caption 都显式列出 | `parent_manifest_sha256=raw`；记录 `scope=motion_physical`，不隐式删除 |
| `semantic_pair_quarantine` | caption 与 motion 错配的精确 pair | `parent_manifest_sha256=raw`；固定 `scope=caption_motion_pair`，不得连带删除同 motion 的其他 caption |
| `clean` | `raw − (physical_quarantine ∪ semantic_pair_quarantine)` 的 order-stable 子序列 | metadata 同时引用 raw 与两份 quarantine SHA256；不得重排、改 ID 或补写样本 |

每份 metadata 至少记录：

- `schema_version`、`manifest_kind`、`revision`、UTC/CST 生成时间、生成代码 commit SHA；
- parent path/SHA256、原始 ordered IDs SHA256、当前 ordered pair IDs SHA256、行数与唯一 pair 数；
- `reason_code_version`、`physical_rule_version`、`semantic_threshold_version`、人工 calibration labels SHA256；
- 所有启用 scorer 的 model name、code revision、checkpoint path/SHA256、preprocess/config SHA256；
- 生成命令、seed、split、输入 manifest hash 与输出 file SHA256。

每条 quarantine record 至少含 `pair_id`、`motion_id`、`caption_id`、raw `order_index`、`scope`、`action=quarantine`、一个或多个 reason code、原始测量值/score、命中阈值及阈值版本、decision source（rule、model agreement 或 manual adjudication）。缺失 checkpoint 的 scorer 不写伪 hash，也不写零分；应在 metadata 中明确记录为 `disabled_missing_checkpoint`。

## 4. 物理规则

所有运动量只在 valid frames、统一单位和 owning geometry decode 下计算。首版候选规则为：

- world-root speed、acceleration、jerk；
- yaw rate 与 yaw acceleration；
- declared foot contact 下的 world foot sliding；
- 地面穿透与持续悬空；
- bone-length drift；
- joint angular velocity/acceleration；
- mesh 可得时的 body self-penetration，以及 environment geometry 可得时的 environment penetration。输入不可得时必须标记该 rule 为 disabled，不能把“未计算”当作通过。

阈值按 capture source、valid-duration bin（`1–64`、`65–128`、`129–192`、`193+`）和可用的动作/locomotion strata 计算 median/MAD robust statistics；小 strata 回退到已记录的上一级分组。数值阈值必须在 calibration 后冻结到 versioned config，本计划不预填未经数据验证的常数。

单一高速值不等于错误。跑、跳、旋转等合法动作不得仅因 root speed 或 yaw rate 高而 quarantine。自动高置信物理 quarantine 至少要求一个直接结构冲突（例如 contact-skating、penetration 或 bone drift）或两个独立动态证据一致；边界值、单证据异常和 locomotion/semantic 冲突进入人工队列。reason code 至少区分 root jerk、yaw spike、contact skating、ground penetration、floating、bone drift、joint kinematics 与 mesh/environment penetration。

## 5. 语义 pair 清洗与 checkpoint 禁令

- 首版自动语义判定只允许 **TMR global alignment + LaMP motion-aware alignment**。二者必须同时有可复现代码、精确 checkpoint 和 SHA256；任一 checkpoint 缺失时，TMR+LaMP 自动 semantic quarantine 整体禁用，只能保留人工审核队列。
- PST 的 joint/segment/global 接口可以预留，但当前没有已登记的可复现 checkpoint，因此状态固定为 `disabled_missing_checkpoint`。不得随机初始化、借用不匹配权重或把论文数值当本地 score。获得并核验 checkpoint 后也必须新建 threshold revision，不能加入已冻结 vote。
- `MARDM-67` 是 evaluator/protocol，不是独立 retrieval scorer，不进入 ensemble vote。
- 只有 TMR 与 LaMP 对同一 pair 方向一致、各自超过人工校准的高精度阈值，且没有人工 veto 时，才允许自动进入 `semantic_pair_quarantine`。模型分歧、只过一个阈值或细粒度关系不确定的样本进入人工队列。
- 语义 reason code 至少覆盖 posture、direction、body-part、temporal order、locomotion、negation 与 global mismatch。错误 caption 只隔离该 pair；同一 motion 的其他 caption 默认保留。

已核验的 pair-level 例子保留为 calibration evidence，而非已执行的 quarantine：`2019_vcdDRblTOmM_00038_001_a` 的 human caption 描述站立并轻微转头；其 GT 仅 `35` 帧，左右膝平均弯曲约 `85.17°/81.82°`，root Z 约 `0.849 m`、root XY displacement 约 `0.056 m`，与持续坐姿/深屈膝一致。gate 打开后，它应作为 semantic review 的明确候选；在此之前不得生成 quarantine record 或改动 manifest。

## 6. `300–500` pair 人工校准

### 6.1 批次声明

- **目标**：校准 conservative quarantine 阈值并估计 false-positive 风险，而不是最大化删除率。
- **来源**：只从 locked raw train parent 采样；不查看 pure4053/test 结果。
- **预算**：目标 `400`，最少 `300`、最多 `500`。
- **输出**：`calibration/labels.jsonl`、`calibration/split.json`、reason-code book、annotator/adjudication audit 及它们的 SHA256。

### 6.2 分层选择

样本同时覆盖：

- 四个 valid-duration bins、主要 capture sources 与 locomotion/non-locomotion；
- physical rule 的 clear-normal、boundary、multi-evidence-high 三个区间；
- TMR/LaMP 均通过、均失败、分歧和接近阈值区间；
- posture、direction、body-part、temporal order、locomotion 与 negation 语义类别。

目标预算的 `70%` 用于 threshold calibration，`30%` 作为冻结后的 holdout audit；两部分保持上述 strata。至少 `20%` pair 双人盲审，分歧经 adjudication 后写入独立字段，不覆盖原标签。

自动 quarantine 的验收以 precision 优先：holdout empirical precision 必须 `≥0.90`，并同时报告置信区间、recall、各 reason/stratum 的样本数。若某 stratum 样本不足、checkpoint 不齐或 precision 未达标，该 stratum 降级为 manual-only，不通过调阈值追逐 holdout。

## 7. Raw-vs-clean 单变量实验

首个 ablation 只改变 Stage2 train manifest：

- **A / raw**：locked `raw` manifest；
- **B / clean**：由同一 raw parent 和冻结 quarantine revisions 得到的 `clean` manifest。

两条 run 必须共享同一 Stage1 checkpoint/owning decoder hash、representation、train-only latent normalization protocol、Unified Stage2 code/backbone、任务概率、seed、optimizer、learning-rate schedule、batch size、总 sample exposures、CFG/sampler、eval ordered IDs 与 decode batch size。clean 数据量较小时用 deterministic resampling 匹配总 exposures，并额外报告 unique pair coverage、重复率和每类 exposure；不得靠少训换取表面优势。两条 cache 的内容 hash 因 manifest 不同而应不同，但 tokenizer checkpoint 和 cache builder revision 必须相同。

正式 eval 使用同一冻结 eval manifest，不把 clean eval 替换成更容易的子集。人工校准 holdout 可作为单独 diagnostic，但不能替代 formal eval。human、camera、joint parallel 与 human-first cascade 均按相同实现/checkpoint 报告：

- human：FDTMR、TMR、HCov，以及 root-aligned/global MPJPE、root ADE/FDE、integrated-yaw error；
- camera：FDCLaTr、CLaTr、CCov、caption F1，以及 Cam-ADE/Cam-FDE/rotation；
- joint：上述适用指标、projection/framing 与 Out；
- no-reference physical：foot contact/skating、acceleration/jerk、bone consistency、root speed/path distributions，并做同 IDs 的 blind render review。

自由生成的 paired MPJPE/Cam-ADE 是 mandatory diagnostic，不单独视为 one-to-many 质量 hard gate。所有 mixed-version 表必须含非空 `version / run` 列。seed-17 matched screen 只能决定是否继续；promotion 至少要用预注册的额外 matched seeds 复核，不能把单 seed screen 写成数据清洗因果定论。

## 8. 验收与 rollback

### 8.1 Manifest 验收

必须全部满足：

1. 四层文件与 sidecar 均存在，SHA256 可重算，parent DAG 无断链；
2. raw 无重复 pair；所有 quarantine pair 都属于 raw；clean 精确满足 set equation 且保持 raw 相对顺序；
3. 每条 quarantine 都有 scope、reason、原始值/score、threshold/checkpoint provenance；
4. semantic pair quarantine 不会删除同 motion 的未命中 caption；motion-level physical action 展开成显式受影响 pairs；
5. 同 input/config 重跑得到相同 ordered IDs 和 hash；
6. 人工 holdout precision gate 通过，未通过的 strata 只进入 review queue。

### 8.2 实验验收

clean 只有在 matched formal 中改善至少一个预注册的 semantic/physical primary diagnostic，且 mandatory human geometry、Cam-ADE/Cam-FDE、distribution/coverage 和 Out 没有超出 raw repeat uncertainty 的系统性退化时，才可成为候选 train manifest。结论必须同时给出逐 seed、aggregate 与 blind render；否则只保留为 diagnostic artifact。

### 8.3 Rollback

rollback 不删除任何文件：将 active data pointer 恢复到 locked raw SHA256，把失败 clean revision 标记为 `rejected_not_active`，停止/隔离由它派生的 cache/run，并保留完整 lineage、失败 gate 和 reason。修正规则或阈值只能从同一 raw parent 产生新 revision；禁止原地编辑 clean 或 quarantine 文件。

## 9. 预注册输出路径

数据产物留在远端 generated run space，不进入 Git：

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/data_curation/storymotion_v8_3_data_curation_20260717/
  contract/curation_contract.json
  manifests/raw.jsonl
  manifests/raw.meta.json
  manifests/physical_quarantine.jsonl
  manifests/physical_quarantine.meta.json
  manifests/semantic_pair_quarantine.jsonl
  manifests/semantic_pair_quarantine.meta.json
  manifests/clean.jsonl
  manifests/clean.meta.json
  calibration/labels.jsonl
  calibration/split.json
  calibration/reason_codebook.json
  scores/physical.jsonl
  scores/tmr.jsonl
  scores/lamp.jsonl
  audit/manifest_lineage.json
  audit/sha256sums.txt
  audit/acceptance.json
  reports/curation_summary.json
```

raw/clean Stage2 训练仍使用标准 run boundary：

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/stage2/v8_3_raw_manifest_unified_SEED_DATE/
/data/public/ripemangobox/Motion/StoryMotion/runs/stage2/v8_3_clean_manifest_unified_SEED_DATE/
```

`SEED`、`DATE`、最终 fixed representation/backbone 和精确 run IDs 在 G0/G5 打开时写入各自 `experiment_contract.json`；当前不得用占位符创建假 run 或假 artifact。
