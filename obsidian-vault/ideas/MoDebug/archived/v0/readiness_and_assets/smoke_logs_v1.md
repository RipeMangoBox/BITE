---
title: "MoDebug P0 Smoke Logs v1"
created: 2026-04-23T01:35
updated: 2026-04-24T22:44
status: archived
tags:
  - Motion_Generation
  - MoDebug
  - p0
  - smoke
related_exec:
  - '[[paperIDEAs/MoDebug/2026-04-22_modebug-exec-plan-alignment-first|MoDebug Exec]]'
---

# MoDebug P0 Smoke Logs v1

## Event-T2M

- 2026-04-23 current-env smoke:
  - command:
    - `conda run --no-capture-output -n event-t2m python src/sample_motion.py repeats=1 device=0 sample_name=taskb_smoke ckpt_path=checkpoints/pretrained/HumanML3D/hml3d.ckpt save_path=./logs/task_b_smoke_sample/ hydra.run.dir=./logs/task_b_smoke_hydra/2026-04-23_run01`
  - result:
    - success
  - key stdout:
    - `Instantiating model <src.models.event_final.EventMotionGeneration>`
    - `Starting generation!`
    - `Done!`
  - artifacts:
    - `[[linkedCodebases/EventT2M-codes-main/logs/task_b_smoke_sample/gen_joints/generated/taskb_smoke_0.npz]]`
    - `[[linkedCodebases/EventT2M-codes-main/logs/task_b_smoke_hydra/2026-04-23_run01/visual.log]]`
    - `[[linkedCodebases/EventT2M-codes-main/logs/task_b_smoke_hydra/2026-04-23_run01/.hydra/config.yaml]]`
- note:
  - 本轮跑的是最小单次 sample smoke，用于确认当前环境与 checkpoint 可用；不是 retrieval-only export。

- found historical eval runs:
  - `[[linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_20-43-20/eval.log]]`
  - `[[linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_20-43-20/metrics.json]]`
  - `[[linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-06_17-12-07/eval.log]]`
- found retrieval artifacts:
  - `[[linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/eval]]`
  - `[[linkedCodebases/EventT2M-codes-main/RUN_DIR/contrastive_metrics.1]]`
- 2026-04-24 adapter smoke:
  - command:
    - `conda run --no-capture-output -n event-t2m python scripts/modebug_eventt2m_adapter_smoke.py`
  - result:
    - pass for `263 -> canonical_22j(+root)` extraction gate
  - key facts:
    - `raw_shape=(199,263)`
    - `canonical_22j_shape=(199,22,3)`
    - `root_shape=(199,3)`
    - `raw_has_nan=False`
    - `joints_has_nan=False`
    - `canonical_rebuild_max_abs=0.0`
    - dataset reference `new_joint_vecs/000000.npy -> new_joints/000000.npy` 逐元素 `max_abs=0.0`
  - artifacts:
    - `[[scripts/modebug_eventt2m_adapter_smoke.py]]`
    - `[[artifacts/modebug/eventt2m_adapter_smoke/modebug_eventt2m_adapter_smoke_report.json]]`
    - `[[artifacts/modebug/eventt2m_adapter_smoke/modebug_eventt2m_adapter_smoke_raw_263.npy]]`
    - `[[artifacts/modebug/eventt2m_adapter_smoke/modebug_eventt2m_adapter_smoke_canonical_22j.npy]]`
    - `[[artifacts/modebug/eventt2m_adapter_smoke/modebug_eventt2m_adapter_smoke_root.npy]]`
  - caveat:
    - 当前 repo 不支持 strict same-`T` `263 <- canonical_22j` 精确逆映射；`process_file()` 不是 import-ready，且 HumanML3D 特征构造会折叠一个 terminal frame。

## ActionPlan

- initial scripted attempt:
  - command intent: `python prepare/download_dependencies.py`
  - result: script failed because bundled call expects `gdown.download(..., fuzzy=True)` but the available `gdown` interface on this machine does not accept `fuzzy`.
- fallback execution:
  - switched to direct `gdown 'https://drive.google.com/uc?id=1q5xd3EARWCoel3iiUKo6YXRJUN34OvYQ' -O actionplan_deps.zip`
  - `actionplan_deps.zip` 已下载并完成解压
- 2026-04-23 minimal inference smoke:
  - command shape:
    - loaded `outputs/actionplan/logs/checkpoints/latest-epoch=9999.ckpt`
    - prompt: `a person walks forward`
    - `seconds=2.0`
    - `steps_per_block=1`
    - `render=False`
  - result:
    - success
    - elapsed: `8.31s`
  - key stdout:
    - `ActionPlan Phase1 (text)`
    - `ActionPlan Phase2 (pyramid)`
    - `LATENTS_SHAPE (15, 16)`
    - `Loaded TAE from .../models/Causal_TAE/net_last.pth`
  - artifacts:
    - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_latents.npy]]`
    - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_decoded272.npy]]`
    - `[[linkedCodebases/ActionPlan-Code/outputs/actionplan/generations/modebug_smoke/walk_forward_smoke_latent_meta.txt]]`
- note:
  - 本轮没有生成 mp4，因此只确认 sample + decode 路径。
- 2026-04-24 minimal supplementary sanity:
  - command family:
    - `conda activate actionplan && python scripts/modebug_actionplan_sanity.py --sample-ids 008463 001969 --output-root artifacts/modebug/actionplan_sanity_min_20260424_run2`
    - `conda activate actionplan && python scripts/modebug_actionplan_sanity.py --sample-ids 004965 --output-root artifacts/modebug/actionplan_sanity_min_20260424_run3`
  - result:
    - second-backbone mechanical proxy path runnable
  - key facts:
    - `streaming` continuation 基本精确保 prefix：
      - `008463`: prefix `0.0 / 0.0`, suffix change `0.184 / 0.245`
      - `001969`: prefix `3.47e-09 / 3.47e-09`, suffix change `0.230 / 0.444`
      - `004965`: prefix `1.91e-09 / 1.91e-09`, suffix change `0.174 / 0.616`
    - 所有成功 run 的 latent / decoded 输出 `finite=true`
  - limitation:
    - 当前只能支持 `G1 + coarse-boundary G3/G5 proxy`
    - 还不能直接给 paper-grade ordering / omission directionality
  - caveat:
    - 此 proxy 仅验证 ActionPlan 的 streaming continuation 机制可运行，不构成 P2/P3/P4 的前置证据
    - exec 要求 Gate 2 闭合前不扩展 P2/P3/P4，此 proxy 不改变该约束
  - artifacts:
    - `[[scripts/modebug_actionplan_sanity.py]]`
    - `[[artifacts/modebug/actionplan_sanity_min_20260424_aggregate.json]]`
    - `[[artifacts/modebug/actionplan_sanity_min_20260424_run2/summary.json]]`
    - `[[artifacts/modebug/actionplan_sanity_min_20260424_run3/summary.json]]`

## ReAlign

- no local smoke output found yet for:
  - reward model training
  - MLD + ReAlign evaluation
- only code-level entrypoints confirmed:
  - `[[linkedCodebases/ReAlign/ReAlignModule/train_spm.py]]`
  - `[[linkedCodebases/ReAlign/test.py]]`

## MotionFix

- local runnable evidence found:
  - evaluator checkpoint:
    - `[[linkedCodebases/motionfix/eval-deps/tmr-evaluator/logs/checkpoints/last.ckpt]]`
  - generation outputs:
    - `[[linkedCodebases/motionfix/experiments/tmed/3way_steps_300_motionfix_noise_last]]`
- 2026-04-24 interface probe:
  - verified:
    - native `pose(135) -> 22j` forward path can run on a short probe without `NaN`
  - not yet verified:
    - `canonical_22j -> pose(135)` bridge
    - `10` oracle-local-edit non-degenerate outputs
    - output回投后的 FID / Diversity drift

## MotionReFit

- local fetch attempt summary:
  - `git lfs pull` failed at index update stage, not at remote download stage.
  - `git lfs fetch` completed and `.git/lfs/objects` 已有对象落地。
- repo repair:
  - executed:
    - `git reset HEAD`
    - `git checkout -- .`
  - result:
    - `git status` 恢复 clean
- current asset state:
  - present:
    - `[[linkedCodebases/motionReFit/data/norm_scaled.npy]]`
    - `[[linkedCodebases/motionReFit/deps/Checkpoints/model_joints_to_smpl_wrist.pth]]`
  - missing:
    - `models/`
    - `models/disc/`
    - `deps/smplx/models`
- still no runnable smoke output found yet because main demo weights are absent.
- repo evidence:
  - `[[linkedCodebases/motionReFit/README.md]]`

## Route-A learned grounding Smoke（2026-04-24 审计后降级）

- status: `deferred`
- note:
  - `ZOMG` 当前只有占位仓库，`TM-Mamba` 未核到官方公开实现
  - 当前周期 Route-A 已冻结为 rule-first coarse checker，不再设置独立的 `Route-A / TMR` smoke gate
  - 如后续进入“自研 learned localizer”分支，再单独新建 smoke 项

## Mainline Interface Chain Status

- `Gate 1: Event-T2M -> canonical_22j`
  - status: `pass`
  - scope:
    - 当前只对 `263 -> canonical_22j(+root)` 无损提取成立
- `Gate 2: canonical_22j -> MotionFix`
  - status: `blocked`
  - blocker:
    - 当前缺的是 `canonical_22j -> SMPL rots/trans -> MotionFix pose(135)` bridge，而不是 MotionFix 本地 checkpoint / dataset
- `Gate 3: MotionFix output -> eval space`
  - status: `blocked-by-dependency`
  - dependency:
    - 依赖 Gate 2 先闭合
