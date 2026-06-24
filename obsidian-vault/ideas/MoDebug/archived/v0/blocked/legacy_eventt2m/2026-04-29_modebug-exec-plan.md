---
created: 2026-04-29T22:47
updated: 2026-05-01T16:05:43+08:00
title: MoDebug Exec Plan：双论文框架下的 Evaluator (Paper A) 与 Generation (Paper B) 并行推进
status: active
tags:
  - MoDebug
  - exec-plan
  - generation
  - evaluator
  - EventT2M
  - ChronAccRet
  - TMR
  - dual-paper
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
  - "[[2026-04-30_modebug-paper-a-eventprobe-plan]]"
  - "[[2026-04-30_modebug-paper-b-perceptguide-plan]]"
  - "[[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]"
---

# MoDebug Exec Plan：双论文框架下的 Evaluator (Paper A) 与 Generation (Paper B) 并行推进

> [!abstract] **执行口径**
> - MoDebug 已拆分为双论文：**Paper A (EventProbe)** evaluator methodology + diagnostic benchmark；**Paper B (PerceptGuide)** 感知增强 reward guidance。
> - 新增 P0：先复现 EventT2M official repo 训练并比较 retrain vs pretrained；未闭合前，Evaluator Exec 与 Generation Exec 都只能写 provisional。
> - 本 exec 中，Evaluator Exec (§1) 归 Paper A，Generation Exec (§2) 归 Paper B。两条线可并行推进，各自独立成文。
> - evaluator 侧已完成 safe-drop consistency / aligned-replace consistency / lexical hard-replace pilot / held-out 分离；generation 侧已完成 G1/G2 attention observation，但现有 artifact 缺 per-head metric，raw attention 暂不进入 reward。
> - 两条线共享 corruption family：`drop / replace / shuffle`。
> - 任何 reward-guided generation 结果都必须同时过 event-side evidence 与 full-level safety。
> - 详细 plan 见 [[2026-04-30_modebug-paper-a-eventprobe-plan|Paper A Plan]] 和 [[2026-04-30_modebug-paper-b-perceptguide-plan|Paper B Plan]]。

## 0. Fixed Inputs

### 0.0 P0 Reproduction Gate

#### P0-G1 EventT2M Clean Retrain

目标：确认官方 pretrained `hml3d.ckpt` 与 clean retrain checkpoint 是否在同一 eval command 下可比。若差异过大，MoDebug 的 eval lane 与 generation lane 都要回退为 provisional。

不要在当前 dirty repo 直接训练。当前 `linkedCodebases/EventT2M-codes-main` 是 fork 且已有 MoDebug instrumentation / diagnostic 脚本修改；retrain 必须使用 clean upstream checkout。

官方 repo 与当前本地状态：

1. upstream：`https://github.com/tjswodud/EventT2M-codes`
2. 当前 symlink：`linkedCodebases/EventT2M-codes-main -> /home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main`
3. 当前本地 repo 有未提交修改，不适合作为 original retrain workspace。
4. 官方 README HumanML3D 训练命令：`trainer.devices="0,1"`、`data.batch_size=128`、`data.repeat_dataset=5`、`trainer.max_epochs=600`、`trainer.precision=bf16-mixed`。

建议 clean retrain workspace：

```bash
cd "/home/ripemangobox/Coding/Github/Motion"
git clone https://github.com/tjswodud/EventT2M-codes.git EventT2M-codes-clean
cd EventT2M-codes-clean
conda create -n event-t2m-clean python==3.10.14
conda activate event-t2m-clean
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

复用本机已有数据和依赖时，优先用 symlink，避免复制：

```bash
ln -s "/home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/deps" deps
mkdir -p dataset
ln -s "/home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/dataset/HumanML3D" dataset/HumanML3D
```

严格 README 版 2-GPU 训练命令：

```bash
python src/train.py trainer.devices=\"0,1\" logger=wandb data=hml3d_event_final \
    data.batch_size=128 data.repeat_dataset=5 trainer.max_epochs=600 \
    callbacks/model_checkpoint=t2m +model/lr_scheduler=cosine model.guidance_scale=4 \
    model.noise_scheduler.prediction_type=sample trainer.precision=bf16-mixed \
    hydra.run.dir=\"logs/event/runs/eventt2m_clean_hml3d_retrain_seed1\"
```

若本机没有 W&B 登录，只把 logger 改成 `logger=tensorboard`；该改动只影响日志后端，不改变训练配置。

本机当前只看到 1×RTX 3090 24GB。单卡 smoke / fallback 命令：

```bash
python src/train.py trainer.devices=\"0,\" logger=tensorboard data=hml3d_event_final \
    data.batch_size=64 data.repeat_dataset=5 trainer.max_epochs=600 \
    callbacks/model_checkpoint=t2m +model/lr_scheduler=cosine model.guidance_scale=4 \
    model.noise_scheduler.prediction_type=sample trainer.precision=bf16-mixed \
    hydra.run.dir=\"logs/event/runs/eventt2m_clean_hml3d_retrain_seed1_b64\"
```

如果 batch 64 仍 OOM，再降到 `data.batch_size=32`，但必须在记录里标注 batch mismatch；它只能验证趋势，不能严格复现官方训练。

注意：upstream `configs/train.yaml` 没有 `exp_name` 字段；不要把本地 fork 的 `exp_name` 写入 original repo 复现实验。上面的 `hydra.run.dir` 只控制日志与 checkpoint 输出目录，不改变训练配置。checkpoint 默认保存在 `${hydra.run.dir}/checkpoints/`。

训练时长预估：

1. 官方论文/README 级配置约为 2×RTX4090、600 epochs、batch 128。没有官方 wall time；本机 1×RTX3090 预估至少数天级，保守估计 `3-7` 天，取决于 dataloader、TMR text embedding cache、验证频率和显存导致的 batch 调整。
2. 建议先跑 `trainer.max_epochs=1` smoke，记录单 epoch wall time，再线性估算 600 epochs。
3. 当前 data_train 为 `24546` samples，`repeat_dataset=5` 后约 `122730` examples/epoch；batch 64 时约 `1918` optimizer steps/epoch，600 epochs 约 `1.15M` steps。

同一 eval command 比较 pretrained vs retrain：

```bash
python src/eval.py trainer.devices=\"0,\" data=hml3d_event_final data.test_batch_size=128 \
    model=event_final model.guidance_scale=4 model.noise_scheduler.prediction_type=sample \
    model.denoiser.stage_dim=\"256*4\" \
    ckpt_path=\"checkpoints/pretrained/HumanML3D/hml3d.ckpt\" \
    retrieval_only=false model.metrics.enable_mm_metric=false \
    hydra.run.dir=\"logs/event/eval/pretrained_hml3d_no_mm\"
```

对 retrain checkpoint 改 `ckpt_path` 为 best checkpoint，例如：

```bash
ckpt_path=\"logs/event/runs/eventt2m_clean_hml3d_retrain_seed1/checkpoints/last.ckpt\"
```

必须记录：

1. `git rev-parse HEAD`
2. train/eval command
3. `data_train.npy / data_val.npy / data_test.npy` path 与 hash
4. GPU 型号、数量、显存
5. wall time 和 peak memory
6. pretrained vs retrain 的 `metrics.json`、`native_normal.yaml`、retrieval YAML 差异

#### P0-G2 ChronAccRet Coverage Fairness

目标：确认 ChronAccRet 的 `event_texts` / `humanml3d_subset` 与 HumanML3D-E 主 test split 的 overlap、uncovered rows 和 event-count bucket 分布。

执行标准：

1. 先生成 coverage audit，不再直接把 ChronAccRet subset 当完整 HumanML3D-E。
2. 主表只允许使用共同可比集合，或明确说明重采样/加权策略。
3. 若 cross-evaluator consistency 保留，必须在每个表里报告 `coverage_tmr`、`coverage_chron`、bucket coverage。

#### P0-G3 Reward-Metric Fairness

目标：把 held-out 从贡献点降级为实验卫生。

规则：

1. 与 reward 高度相似的 metric 只能是 `dev_metric`。
2. 使用同源 scorer/protocol 做训练、selection 或 inference-time enhancement 后，不能再把它写成 final improvement。
3. Paper B 的贡献不包含 held-out rule；只包含 event-marginal reward 和 inference-time correction。

### 0.1 主数据

1. 主数据源：`HumanML3D-E`
2. event decomposition cache：
   - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_train.json`
   - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_val.json`
   - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_test.json`
3. 第一批 seed pool：
   - `004965`
   - `008463`
   - `001969`
   - `003245`
4. 后续 observation pool：优先抽 `40-80` 条 HumanML3D-E test split 中 `>=3 events` 样本。
5. 已固定 observation pool：
   - `linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl`
   - `linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/summary.json`
   - `64` 条 HumanML3D-E test `>=3 events` 样本，固定 seed 完整，`5plus` 高风险 bucket `28` 条。

### 0.2 固定模块角色

| 模块 | 当前角色 | 不能承担什么 |
| --- | --- | --- |
| Event-T2M | generation backbone；self eval sanity | event-level judge |
| native TMR | omission / semantic side signal | formal ordering；duration；standalone final judge |
| ChronAccRet | formal ordering evidence；omission cross-check | duration；完整 HumanML3D-E 覆盖 |
| AToM | MotionGPT native eval reproduction record | 当前 MoDebug 主 judge |
| attention filter | interval miner / evaluator router / observation layer | raw attention final judge |

## 1. Evaluator Exec ← Paper A (EventProbe)

### E0. Freeze Current Evidence

状态：done。

必须引用的 artifact：

1. Event-T2M self eval 数值见 [[2026-04-29_modebug-evaluator-status-summary|Evaluator Status Summary]]。
2. native TMR omission：
   - `linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/summary.json`
   - `linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/bucket_summary.json`
3. ChronAccRet ordering：
   - `linkedCodebases/ChronAccRet/output/bert_orig/subset_eval/shuffle_event.yaml`
4. ChronAccRet omission：
   - `linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_event.yaml`
   - `linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_rows.jsonl`

验证标准：

1. summary note 明确写成 `ChronAccRet omission protocol 已补齐`。
2. TMR 只写成 omission side signal。
3. AToM 不进入当前主 judge。

### E1. Join Diagnostics + Safe-Drop Consistency

状态：done。

目标：确认 native TMR 与 ChronAccRet omission 是否能互相支撑，而不是各自孤立。

实际完成 protocol：

1. 读取 TMR `omission_rows.jsonl`。
2. 读取 ChronAccRet `omission_rows.jsonl`。
3. 使用 safe-drop join，不硬凑 replace mismatch：
   - `sample_id/keyid`
   - `target_idx`
   - `event_count`
   - `dropped_event`
   - `full_text`
   - `drop_text`
4. 输出统计：
   - TMR 与 ChronAccRet 对 `full_vs_drop_paired_acc` 判定的 agreement。
   - agreement 按 event_count 的 `2 / 3 / 4 / 5plus` bucket。
   - disagreement 样本 top cases，供 human review。
   - join coverage 与 replace mismatch limitation。

已完成输出：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/summary.json`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/join_diagnostics.json`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/disagreement_cases.jsonl`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/top_cases.md`

当前结论：

1. safe-drop comparable rows：`1608`
2. agreement：`1179 / 1608 = 73.32%`
3. `5plus` agreement：`51 / 80 = 63.75%`
4. coverage：vs TMR `42.33%`，vs ChronAccRet `68.92%`
5. safe-drop consistency 不覆盖 replace corruption。

### E2. Held-Out Eval Separation

状态：done。

输出：[[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]]。

硬规则：

1. 如果 `R_pres` reward 使用 TMR，最终 omission eval 优先用 ChronAccRet omission 或 human eval。
2. 如果 `R_pres` reward 使用 ChronAccRet，最终 omission eval 优先用 TMR 或 human eval。
3. 如果 `R_ord` reward 使用 ChronAccRet，最终 ordering 主证据需要 human eval 或另一个独立 scorer；否则 ChronAccRet 只能写 development metric。
4. Event-T2M self eval 始终只作 full-level safety，因为它不是 event reward scorer。
5. 被用作 reward 的 scorer/protocol 不能同时作为 final main-table evaluator/protocol。

### E3. Aligned-Replace Consistency

状态：done。

目标：修复原先 TMR 与 ChronAccRet replace corruption 不可比较的问题，用同一 deterministic replacement manifest 重新打分。

已完成输出：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_manifest.jsonl`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/tmr_aligned_replace_rows.jsonl`
3. `linkedCodebases/ChronAccRet/output/bert_orig/aligned_replace_eval/chronaccret_aligned_replace_rows.jsonl`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_consistency_summary.json`

当前结论：

1. manifest rows：`1608`
2. `tmr_safe_subset_pres_full_vs_aligned_replace_paired_acc = 0.835820895522388`
3. `chron_subset_pres_full_vs_aligned_replace_paired_acc = 0.8538557213930348`
4. agreement：`1313 / 1608 = 81.65%`
5. `5plus` agreement：`63 / 80 = 78.75%`

边界：这是 replacement corruption 的 evaluator-side cross-check，不是 standalone final judge。

coverage 限制：aligned-replace 仍只覆盖 TMR rows 的 `42.33%` 与 ChronAccRet rows 的 `68.92%`，不能外推到全部 TMR omission rows。

### E3b. Lexical Hard-Replace Stress Pilot

状态：done for 512-row lexical pilot；TMR embedding hard negative pending。

目标：检查 aligned-replace 是否因为 negative 太 easy 而高估 evaluator 区分度。

已完成输出：

1. `linkedCodebases/EventT2M-codes-main/src/run_modebug_hard_replace_manifest.py`
2. `linkedCodebases/EventT2M-codes-main/src/run_modebug_tmr_hard_replace_eval.py`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/hard_replace_manifest_summary.json`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json`
5. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_rows.jsonl`

当前结论：

1. manifest rows：`512`
2. candidate backend：`lexical`
3. `tmr_gt_pres_hard_replace_lexical_paired_acc = 0.65234375`
4. old `tmr_safe_subset_pres_full_vs_aligned_replace_paired_acc = 0.835820895522388`
5. delta：`-0.18347714552238803`
6. `5plus` bucket：`15 / 27 = 0.5555555555555556`

边界：这只证明 easy-negative 膨胀风险成立，不替代正式 evaluator。若要把 hard-replace 写成强实验，需要再跑 `--candidate-backend tmr` 或补 ChronAccRet hard-replace scoring。

### E4. Full-Level Safety Check Post-G4

状态：pending after G4。

目标：保证 event-side gain 不破坏 full-level generation sanity。

最小 protocol：

1. baseline Event-T2M generation 保留 FID / R-Precision / matching score。
2. guidance 版本生成同一批样本后，跑同一套 Event-T2M self eval。
3. 报告 full-level delta，同时报告 TMR / ChronAccRet event-side delta。

通过标准：

1. Event-side 指标改善不能以 full-level FID 明显恶化为代价。
2. 如果 full-level safety 不过，只能写 observation 或 failure analysis，不能写主表提升。

## 2. Generation Exec ← Paper B (PerceptGuide)

### G0. Observation Pool

状态：done。

样本来源：

1. 固定 seed：`004965 / 008463 / 001969 / 003245`
2. 扩展 pool：HumanML3D-E test split 中 `>=3 events` 的 `40-80` 条样本。
3. 高风险 bucket：优先加入 `5plus` event cases，因为 TMR bucket 里信号最弱。

输出：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/summary.json`
3. `64` 条 HumanML3D-E test split `>=3 events` 样本。
4. `5plus` 高风险 bucket `28` 条。
5. planned conditions：`full / drop / replace / shuffle`。
6. condition manifest：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/condition_manifest.jsonl`，`256` rows。

### G1. Attention Map Observation

状态：instrumentation + 256-row logging done。

目标：判断 Event-T2M 内部 event condition 是否对应 motion 的不同 temporal regions。

可用依据：

1. Event-T2M 内部 `MiniConformer.cross_attn` 的 query 是 patch-level motion tokens，key/value 是 decomposed event tokens，适合做 G1/G2 observation。
2. 已新增 opt-in logging：打开 `need_weights=True`、`average_attn_weights=False`，默认 sample path 不变。
3. 已完成 `64` samples x `4` conditions 的 step10 run。

最小日志字段：

```yaml
sample_id: "004965"
event_idx: 2
event_text: "a person picks something up."
condition: "full_original"
attn_peak_t: 0.42
attn_interval: [0.31, 0.52]
attn_mass_top_interval: 0.37
attn_entropy: 1.84
relative_gap_vs_generic: 0.12
relative_gap_vs_corrupted: 0.19
order_peak_rank: 2
flag:
  - candidate_middle_event
```

通过标准：

1. attention 不是固定位置偏置。
2. success samples 的 temporal separation 明显强于 failure samples。
3. `drop / replace / shuffle` 会导致方向正确的 attention 变化。
4. 原始 attention peak 不写成正式 evaluator 或 ordering metric。

当前结果：

1. artifact：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/observations.jsonl`
2. analysis：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/g1g2_observation_analysis_summary.json`
3. filtering analysis：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/head_filtering_analysis.json`
4. rows：`256`
5. attention records：`10240`
6. finite failures：`0`
7. full normalized entropy mean：`0.9962925080675632`
8. condition-order peak match：`0.05234375`
9. per-head metric availability：`false`

判断：raw attention 工程链路可用，但现有 `observations.jsonl` 没有 `head` / `head_idx` / per-head metric，只保留 shape `[2, 8, 25, 11]` 和 head-averaged summary。当前 filtering verdict 为 `blocked_no_per_head_artifact`，所以不能宣称已经完成真正 per-head filtering；若继续内部 attention path，先改 logging 保存 per-head metric，再小规模重跑。

### G2. Denoising Trajectory Observation

状态：step10 logging done。

目标：决定 reward guidance 的介入时机。

要记录：

1. 每个 event 的 attention peak 在 diffusion steps 中何时出现。
2. 后 emerge 的 event 是否更容易 omission。
3. 早期 intervention 是否比后期 intervention 更可能改变 event coverage。

通过标准：

1. 能观察到稳定的 emergence pattern。
2. 如果 trajectory signal 混乱，先不接 trajectory-aware guidance。

当前判断：step10 trajectory 已记录，但 raw layer-level attention entropy 高，且缺 per-head metric，暂不能作为 trajectory-aware guidance 依据。

### G3. Gradient Sensitivity Observation

状态：feasibility confirmed via code analysis；frozen-forward diagnostic implementation pending。

目标：确认 event text condition 是否对 motion 的局部时间段有控制力。

只做：

1. 对 frozen generated motion 计算 gradient。
2. 记录 event condition 对 frames / latent timesteps 的 gradient mass。
3. 比较 full / drop / replace / shuffle 条件。

不做：

1. 不更新 backbone。
2. 不把 gradient sensitivity 写成正式 evaluator。
3. 不直接用 raw gradient 做 final reward。
4. 不直接复用默认 `sample_motion()` 取梯度，因为该入口被 `@torch.no_grad()` 包住；只能在窄作用域 frozen forward 中局部启用 gradient。

### G1-G3 Shared Observation Schema

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/schema.yaml`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/README.md`
3. [[2026-04-29_modebug-attention-extraction-feasibility|Attention Extraction Feasibility]]
4. [[2026-04-30_modebug-render-video-mllm-sidecar-feasibility|Render-to-Video + MLLM Sidecar Feasibility]]

边界：G1/G2 现在已有 logging artifact，但仍只是 observation，不是直接可跑 reward，也不是正式 judge。G3 仍是 implementation pending；如果不先补 per-head logging，G3 的优先级低于 sidecar pilot。

### G4. Inference-Time Guidance MVP

进入条件：

1. E1 safe-drop consistency 与 E3 aligned-replace consistency 不失败。
2. E2 held-out eval rule 已写清楚。
3. G1/G2 raw signal 经过 per-head logging 小重跑或 sidecar 后显示稳定 counterfactual sensitivity。
4. G3 frozen-forward gradient sensitivity 至少完成 diagnostic。
5. MVP 先限制在 `3-4` event 样本；`5plus` safe-drop agreement `63.75%`、hard-replace TMR `55.56%`，当前不足以支撑 reward guidance。

最小实现：

1. 先只开小权重 `R_pres`。
2. `R_ord` 只在 independent final eval 可用时接入。
3. 每个 guidance run 同时记录 full-level safety 与 event-side evidence。

退出条件：

1. guidance 梯度爆炸。
2. Event-T2M self eval 明显退化。
3. reward scorer 上升但 held-out evaluator 不升。

## 3. Parallelization Rule（双论文并行依赖）

可以并行：

1. evaluator 侧可继续 E3b 的 TMR-embedding hard-negative 或 ChronAccRet hard-replace cross-check。
2. generation 侧可并行做 per-head logging 小重跑与 render-to-video MLLM sidecar pilot。
3. 文档侧可同步维护 coverage、5plus、held-out 边界，不等待新训练。

不能并行跳过：

1. 不能在 E1 + E2 + per-head/sidecar signal + G3 之前直接上 guidance。
2. 不能把 observation signal 写成正式 evaluator。
3. 不能用同一个 scorer/protocol 同时做 reward 和 final 主表。
4. 不能把 `5plus` bucket 纳入 G4 MVP reward guidance，除非后续 evaluator consistency 显著改善。


### 跨论文并行依赖表

| Paper A 任务 | Paper B 任务 | 关系 |
|---|---|---|
| A-EXP1 多 baseline 诊断 | B-EXP1 reward model 训练 | 完全并行，互不阻塞 |
| A-EXP2 evaluator leakage | B-EXP1 reward model 训练 | 完全并行 |
| A-EXP3 hard-negative replace | B-EXP1 reward model 训练 | 完全并行；A-EXP3 结果可选择性反馈给 B-EXP1 的负例策略 |
| A-EXP5 failure pattern | B-EXP2 discriminative pilot | 完全并行 |
| A-EXP2 evaluator leakage | B-EXP5 held-out evaluation | B-EXP5 最好等 A-EXP2 结论（决定 reward/held-out 分配），但 B 可用默认分配独立进行 |
| A-EXP4 human eval | B-EXP3 guidance injection | 完全并行 |
| A 写作 | B 写作 | 完全并行；B 可引用 A 的 evaluation protocol，也可自包含描述 |

B 独立成文条件：B 自己在 related work 中描述 held-out separation principle + 自己跑 TMR/ChronAccRet cross-check + evaluation section 自包含描述 corruption protocol。

A 独立成文条件：A 完全不依赖 B，所有实验都是 evaluation-side。

## 4. Current Non-Goals

1. 不扩 ordering。
2. 不补 duration evaluator。
3. 不自建 judge。
4. 不引入 MotionPatches。
5. 不把 RL primer 或 PAPO-lite debug 作为当前 exec 主线。
