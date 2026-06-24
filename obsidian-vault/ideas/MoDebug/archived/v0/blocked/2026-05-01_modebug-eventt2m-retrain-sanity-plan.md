---
created: 2026-05-01T16:05:43+08:00
updated: 2026-05-11T20:55:00+08:00
title: MoDebug EventT2M Retrain Sanity Record
status: superseded
tags:
  - MoDebug
  - EventT2M
  - retrain
  - reproducibility
  - p0-gate
  - status/superseded
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[2026-05-01_modebug-unified-ideas-progress]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]"
  - "[[ideas/MoDebug/blocked/README]]"
---

# MoDebug EventT2M Retrain Sanity Record

> [!warning] Superseded For Backbone Selection
> This note is a historical record of EventT2M paper-native full-level reproducibility. The later 2026-05-11 `2ac5ea8` revalidation restored the `003245` epoch135 single-sample scale sanity, but that record is still diagnostic only. Do not use this note as current S7/S8/S10 backbone evidence.

## Purpose

This record documents the completed clean retrain and paper-metric sanity checks for released EventT2M pretrained `hml3d.ckpt`. Its current scope is historical: it explains why the checkpoint was not suspicious under paper-native full-level metrics, not whether current generated motions are usable for MoDebug.

Current decision: **superseded for backbone selection**. Released EventT2M `hml3d.ckpt` and retrain `epoch_135` are historical reproducibility assets. Re-entering EventT2M into active MoDebug requires a fresh active protocol, not this note.

This closes only the old pretrained/retrain full-level reproducibility uncertainty. It does not prove MoDebug's counterfactual event-level correctness, event-conditioned backbone suitability, or final evaluator safety.

## Current Local Facts

1. Active dirty repo: `linkedCodebases/EventT2M-codes-main -> /home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main`.
2. Current repo has MoDebug modifications and untracked diagnostic scripts; do not train original reproduction there.
3. Upstream official repo: `https://github.com/tjswodud/EventT2M-codes`.
4. Current visible GPU: `1 x NVIDIA GeForce RTX 3090 24GB`.
5. Local HumanML3D / HumanML3D-E splits are present:
  - train: `24546`
  - val: `1530`
  - test: `4646`
6. Official README HumanML3D command uses 2 GPUs, batch `128`, repeat_dataset `5`, max_epochs `600`, bf16 mixed precision.

## Clean Setup Used

```bash
cd "/home/ripemangobox/Coding/Github/Motion"
git clone https://github.com/tjswodud/EventT2M-codes.git EventT2M-codes-clean
cd EventT2M-codes-clean

conda create -n event-t2m-clean python==3.10.14
conda activate event-t2m-clean
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

Reuse local data/deps by symlink:

```bash
ln -s "/home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/deps" deps
mkdir -p dataset
ln -s "/home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/dataset/HumanML3D" dataset/HumanML3D
```

## Training Command Used

Official README-style 2-GPU command:

```bash
python src/train.py trainer.devices=\"0,1\" logger=wandb data=hml3d_event_final \
    data.batch_size=128 data.repeat_dataset=5 trainer.max_epochs=600 \
    callbacks/model_checkpoint=t2m +model/lr_scheduler=cosine model.guidance_scale=4 \
    model.noise_scheduler.prediction_type=sample trainer.precision=bf16-mixed \
    hydra.run.dir=\"logs/event/runs/eventt2m_clean_hml3d_retrain_seed1\"
```

Do not pass `exp_name` for the clean upstream repo; that key exists in the local fork, not in the official config. `hydra.run.dir` only fixes the output directory. Training checkpoints are written to `${hydra.run.dir}/checkpoints/`.

## Training Time Record

Actual completed run:

1. official README-style 2-GPU command with batch `128`, repeat_dataset `5`, max_epochs `600`, and bf16 mixed precision.
2. wall time: approximately `2026-05-01 16:19` to `2026-05-02 07:25`, about `15.1` hours.

## Evaluation Commands Used

Evaluate released pretrained checkpoint:

```bash
python src/eval.py trainer.devices=\"0,\" data=hml3d_event_final data.test_batch_size=128 \
    model=event_final \
    model.guidance_scale=4 model.noise_scheduler.prediction_type=sample \
    model.denoiser.stage_dim=\"256*4\" \
    ckpt_path=\"checkpoints/pretrained/HumanML3D/hml3d.ckpt\" \
    retrieval_only=false model.metrics.enable_mm_metric=false \
    hydra.run.dir=\"logs/event/eval/pretrained_hml3d_no_mm\"
```

Evaluate retrain checkpoint:

```bash
python src/eval.py trainer.devices=\"0,\" data=hml3d_event_final data.test_batch_size=128 \
    model=event_final \
    model.guidance_scale=4 model.noise_scheduler.prediction_type=sample \
    model.denoiser.stage_dim=\"256*4\" \
    ckpt_path=\"logs/event/runs/eventt2m_clean_hml3d_retrain_seed1_b64/checkpoints/last.ckpt\" \
    retrieval_only=false model.metrics.enable_mm_metric=false \
    hydra.run.dir=\"logs/event/eval/retrain_hml3d_b64_no_mm\"
```

The completed standard sanity run evaluated released `pretrained`, `epoch_135`, `epoch_230`, `epoch_237`, `epoch_288`, `epoch_325`, and `last` checkpoints under the same native metric command family.

## Decision Criteria Applied

| Check | Result | Decision |
| --- | --- | --- |
| Released pretrained vs PDF Table 1 | close on HumanML3D FID / R@3 / matching | released checkpoint is not suspicious |
| Clean retrain vs released pretrained | same-scale native full-level metrics; `epoch_135` stronger on standard eval | retrain confirms backbone reproducibility |
| Released pretrained vs PDF Table 3 | condition2/3/4 metrics basically reproduced | event-count subset hygiene is acceptable |
| MoDebug counterfactual event correctness | not covered by this sanity record | must be tested by S7/S10 diagnostics |


## 2026-05-02 Result

Verdict: **pass for native full-level training hygiene**.

The released pretrained checkpoint is close to the PDF Table 1 HumanML3D metrics, and the clean retrain is not suspicious relative to the released pretrained checkpoint under the same native EventT2M evaluation protocol. At least two retrain checkpoints are directly comparable:

1. `pretrained`: local FID `0.04765`, R@3 `0.8418`, matching `2.7150`; PDF Table 1 reports FID `0.056±.002`, R@3 `0.842±.002`, MM-Dist `2.711±.005`.
2. `epoch_135`: better FID, R@3, and matching score than pretrained in this single-replication sanity run.
3. `epoch_325`: almost identical FID to pretrained (`1.02x`) and slightly higher R@3.

This closes the specific concern that the released pretrained `hml3d.ckpt` is likely manipulated or unreproducible under paper-native full-level metrics. It does not, by itself, confirm current MoDebug backbone usability; later EventT2M revalidation must be cited through [[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]].

Run facts:

1. train command: official README-style HumanML3D command with `trainer.devices="0,1"`, `logger=wandb`, `data.batch_size=128`, `data.repeat_dataset=5`, `trainer.max_epochs=600`, bf16 mixed precision.
2. train wall time: approximately `2026-05-01 16:19` to `2026-05-02 07:25`, about `15.1` hours.
3. train repo HEAD: `196a11811178a61b722c7f838e843df840d72c8f`; upstream/main at check time: `40fe01856b17d7388fc9004b9f46cb234a704b9f`.
4. eval command family: `src/eval_native_only.py`, same native EventT2M eval logic as upstream `src/eval.py`, with `data=hml3d_event_final`, `data.test_batch_size=128`, `model=event_final`, `model.guidance_scale=4`, `model.noise_scheduler.prediction_type=sample`, `model.denoiser.stage_dim=256*4`, `model.metrics.enable_mm_metric=false`, `model.metrics.replicate_times=1`.
5. eval environment repair: `event-t2m` env had drifted to `numpy==2.2.6`, which broke SciPy / torchmetrics import. It was restored to `numpy==1.26.4`, matching the training W&B requirements snapshot and SciPy `1.11.1` compatibility.
6. eval output root: `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/`.


| ckpt         | FID↓    | ΔFID     | FID/pre | R@1↑   | R@2↑   | R@3↑   | ΔR@3    | Match↓ | ΔMatch  | Div    | metrics.json                                                                                          |
| ------------ | ------- | -------- | ------- | ------ | ------ | ------ | ------- | ------ | ------- | ------ | ----------------------------------------------------------------------------------------------------- |
| `pretrained` | 0.04765 | ref      | 1.00x   | 0.5552 | 0.7522 | 0.8418 | ref     | 2.7150 | ref     | 9.5750 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/pretrained/metrics.json` |
| `epoch_135`  | 0.04064 | -0.00701 | 0.85x   | 0.5614 | 0.7541 | 0.8478 | +0.0060 | 2.6923 | -0.0227 | 9.3271 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/epoch_135/metrics.json`  |
| `epoch_230`  | 0.06210 | +0.01445 | 1.30x   | 0.5603 | 0.7575 | 0.8446 | +0.0028 | 2.6994 | -0.0156 | 9.3927 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/epoch_230/metrics.json`  |
| `epoch_237`  | 0.05710 | +0.00945 | 1.20x   | 0.5515 | 0.7459 | 0.8345 | -0.0073 | 2.7536 | +0.0386 | 9.6133 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/epoch_237/metrics.json`  |
| `epoch_288`  | 0.05590 | +0.00825 | 1.17x   | 0.5567 | 0.7504 | 0.8397 | -0.0022 | 2.7220 | +0.0070 | 9.2024 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/epoch_288/metrics.json`  |
| `epoch_325`  | 0.04872 | +0.00107 | 1.02x   | 0.5530 | 0.7470 | 0.8431 | +0.0013 | 2.7053 | -0.0097 | 9.6817 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/epoch_325/metrics.json`  |
| `last`       | 0.06417 | +0.01652 | 1.35x   | 0.5662 | 0.7547 | 0.8358 | -0.0060 | 2.6948 | -0.0202 | 9.7544 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/last/metrics.json`       |


Interpretation:

1. The top-k retrain checkpoints are stable and close to pretrained on native metrics.
2. FID varies across saved epochs, but this is checkpoint-selection noise rather than a backbone-level failure: best retrain `epoch_135` is better than pretrained; closest retrain `epoch_325` is effectively tied with pretrained.
3. Retrieval quality is not degraded at the level that would invalidate MoDebug: retrain R@3 ranges from `0.8345` to `0.8478` vs pretrained `0.8418`.
4. Matching score is also same-scale; several retrain checkpoints are slightly better than pretrained.
5. Use `epoch_135` as best native sanity checkpoint and `epoch_325` as pretrained-matched sanity checkpoint when a retrain baseline is needed.

## 2026-05-02 HumanML3D-E Condition Result

Verdict: **pass for EventT2M paper-native condition2/3/4 reproducibility**.

This section covers EventT2M's own HumanML3D-E event-count subset protocol from Table 3 / Table 13. It is not MoDebug's counterfactual diagnostic protocol.

Run facts:

1. eval output root: `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/`.
2. data root: temporary symlink roots under `linkedCodebases/EventT2M-codes-main/tmp/modebug_condition_eval/{condition2,condition3,condition4}/HumanML3D/`, where `data_test.npy` points to the corresponding official `data_test_condition*.npy`.
3. eval command family: `src/eval_native_only.py`, `data=hml3d_event_final`, `data.test_batch_size=128`, `model=event_final`, `model.guidance_scale=4`, `model.noise_scheduler.prediction_type=sample`, `model.denoiser.stage_dim=256*4`, `model.metrics.enable_mm_metric=false`, `model.metrics.replicate_times=1`.
4. MModality is not compared because this sanity run disables `enable_mm_metric`; condition4 native Diversity is `-1.0` due the small subset.

| Condition | ckpt | FID↓ | ΔFID vs paper | R@1↑ | R@2↑ | R@3↑ | ΔR@3 vs paper | Match↓ | ΔMatch vs paper | metrics.json |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| C2 | `paper` | 0.07900 | ref | 0.5360 | 0.7320 | 0.8240 | ref | 2.8360 | ref | PDF Table 3 |
| C2 | `pretrained` | 0.07883 | -0.00017 | 0.5328 | 0.7303 | 0.8241 | +0.0001 | 2.8228 | -0.0132 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition2/pretrained/metrics.json` |
| C2 | `epoch_135` | 0.06317 | -0.01583 | 0.5421 | 0.7427 | 0.8376 | +0.0136 | 2.7828 | -0.0532 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition2/epoch_135/metrics.json` |
| C2 | `epoch_325` | 0.07308 | -0.00592 | 0.5424 | 0.7350 | 0.8202 | -0.0038 | 2.8079 | -0.0281 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition2/epoch_325/metrics.json` |
| C3 | `paper` | 0.13700 | ref | 0.4870 | 0.6870 | 0.7900 | ref | 2.9280 | ref | PDF Table 3 |
| C3 | `pretrained` | 0.14405 | +0.00705 | 0.5089 | 0.6964 | 0.7868 | -0.0032 | 2.9188 | -0.0092 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition3/pretrained/metrics.json` |
| C3 | `epoch_135` | 0.12279 | -0.01421 | 0.5000 | 0.7121 | 0.8058 | +0.0158 | 2.8701 | -0.0579 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition3/epoch_135/metrics.json` |
| C3 | `epoch_325` | 0.16867 | +0.03167 | 0.5156 | 0.7020 | 0.8013 | +0.0113 | 2.9180 | -0.0100 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition3/epoch_325/metrics.json` |
| C4 | `paper` | 0.26500 | ref | 0.4660 | 0.6600 | 0.7670 | ref | 3.0630 | ref | PDF Table 3 |
| C4 | `pretrained` | 0.26238 | -0.00262 | 0.4805 | 0.6641 | 0.7578 | -0.0092 | 3.0082 | -0.0548 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition4/pretrained/metrics.json` |
| C4 | `epoch_135` | 0.29793 | +0.03293 | 0.4531 | 0.6680 | 0.7617 | -0.0053 | 2.9627 | -0.1003 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition4/epoch_135/metrics.json` |
| C4 | `epoch_325` | 0.36483 | +0.09983 | 0.4648 | 0.6523 | 0.7773 | +0.0103 | 3.0703 | +0.0073 | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/condition4/epoch_325/metrics.json` |

Interpretation:

1. Released pretrained almost exactly matches the paper on C2, is close on C3, and is close on C4 FID / matching with a small R@3 drop.
2. `epoch_135` is stronger than pretrained on C2/C3, but C4 FID is worse while R@3 remains close; this is acceptable subset-level variance for a sanity run.
3. `epoch_325` remains usable as a pretrained-matched retrain checkpoint on C2/C3 retrieval, but its C4 FID is worse; do not use it as the best condition baseline.
4. Historical interpretation at the time was to use released pretrained as the primary backbone and `epoch_135` as the preferred retrain baseline. This interpretation remains superseded for active MoDebug claim selection; use the 2026-05-11 revalidation log for the later diagnostic scale-sanity repair.

## Backbone Decision

Decision: **superseded for generated-motion backbone selection**. Keep released EventT2M `hml3d.ckpt` and retrain checkpoints as historical full-level reproducibility records only.

Scope:

1. Confirmed: native HumanML3D full-level reproducibility and HumanML3D-E condition2/3/4 paper-native reproducibility.
2. Not confirmed: MoDebug counterfactual event-level correctness, omission sensitivity under `drop_text`, replacement sensitivity, shuffle/order sensitivity, duration judgment, or reward/evaluator fairness.
3. Required follow-up: do not keep EventT2M pretrained / retrain as required S7 backbone columns unless a new active protocol reports current data, checkpoint, sampling config, generated-motion sanity, evaluator coverage, `n/evaluable`, and limitations.

## Drift Note

2026-05-02:

old_plan -> EventT2M retrain sanity pending; both lanes blocked by pretrained/retrain uncertainty

new_plan -> EventT2M native full-level and HumanML3D-E condition2/3/4 hygiene passed; released pretrained is close to PDF Table 1 / Table 3 and clean retrain is same-scale; at the time this was interpreted as sufficient backbone hygiene, but that interpretation is now superseded for generated-motion use

evidence -> PDF Table 1 HumanML3D Event-T2M reports FID `0.056±.002`, R@3 `0.842±.002`, MM-Dist `2.711±.005`; local pretrained has FID `0.04765`, R@3 `0.8418`, matching `2.7150`; PDF Table 3 C2/C3/C4 paper FID/R@3 = `0.079/0.824`, `0.137/0.790`, `0.265/0.767`; local pretrained = `0.07883/0.8241`, `0.14405/0.7868`, `0.26238/0.7578`; `epoch_135` retrain has standard FID `0.04064` and R@3 `0.8478`

affected_docs -> README, Unified Ideas Progress, this retrain sanity plan

next_action -> start ChronAccRet HumanML3D-E domain alignment, reward model prep, per-head / gradient attribution, and multi-baseline diagnostics

2026-05-06:

old_plan -> use released EventT2M `hml3d.ckpt` as primary backbone and `epoch_135` as retrain sanity column

new_plan -> treat this note as historical full-level reproducibility only; later scale-sanity repair is recorded separately and does not promote this note to active backbone evidence

evidence -> superseded diagnostic details are preserved in the 2026-05-06 historical record; the current revalidation record is [[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]

affected_docs -> README, Unified Ideas Progress, Backbone Migration Plan, S7 component summary

next_action -> use a new active route note before citing EventT2M generated motions in S7/S8/S10

2026-05-01:

old_plan -> treat official pretrained EventT2M as fixed backbone

new_plan -> make EventT2M retrain sanity a P0 gate before paper-level claims

evidence -> both evaluator and generation lanes depend on EventT2M; current local repo is dirty; official README specifies retrain command

affected_docs -> README, Roadmap, Exec Plan, Paper A, Paper B

next_action -> superseded by 2026-05-02 result; clean retrain and eval are complete
