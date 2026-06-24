---
title: "MoDebug P0 Missing Assets Report v1"
created: 2026-04-23T01:35
updated: 2026-04-26T02:31
status: archived
tags:
  - Motion_Generation
  - MoDebug
  - p0
  - blockers
related_exec:
  - '[[paperIDEAs/MoDebug/2026-04-22_modebug-exec-plan-alignment-first|MoDebug Exec]]'
---

# MoDebug P0 Missing Assets Report v1

## Baseline Blockers

### ReAlign-MLD

- missing:
  - `checkpoints/mld_humanml/mld_humanml_v1.ckpt`
  - default SPM checkpoint
  - host + reward model smoke output
- verified source:
  - ReAlign README OneDrive / Baidu share 已定位
  - repo 级 deps / datasets 已在本地补齐
  - MotionLCM 下载脚本可作为 `glove / t2m / smpl_models / pretrained mld` 的 fallback 来源
  - 当前环境访问其官方 OneDrive share 会返回 `The request is blocked`

### MotionReFit

- missing:
  - smoke output
  - STANCE dataset 本地根
- current blocker:
  - repo/index inconsistency 已修复；Hugging Face demo weights 与 SMPL-X model assets 已补齐，当前真正阻塞项变成 smoke 验证与 STANCE dataset

## Dataset Blockers

### 272-dim-HumanML3D

- missing:
  - `1918` train split motion files
- effect:
  - train split 不能视作 fully ready，当前只能按 `partial` 记账

### BABEL

- missing:
  - local dataset root
  - preprocess output
  - split audit result

### TEACH

- missing:
  - local dataset root
  - preprocess output
  - split audit result
- note:
  - `teach` repo 已获取，但数据仍依赖 AMASS/BABEL/TEACH website/SMPLH 组合链路，无法在当前轮自动闭合

### FineMotion

- resolved on 2026-04-26:
  - standalone local dataset root 已 materialize：
    - `[[linkedCodebases/datasets/FineMotion/BPMP_auto.json]]`
    - `[[linkedCodebases/datasets/FineMotion/BPMP_human.json]]`
    - `[[linkedCodebases/datasets/FineMotion/BPMSD_auto.json]]`
    - `[[linkedCodebases/datasets/FineMotion/BPMSD_human.json]]`
- residual risk:
  - 该 root 只闭合了 FineMotion 文本标注层，底层 motion 仍继承 `HumanML3D`
  - `BPMSD_human.json` 仍不足以直接声明 clean body-part single-label ground truth fully ready

## Non-Blocking Paper-Only References

### FineXtrol

- status:
  - paper-only
- note:
  - 本地 repo 已获取，但官方 README 明确 `Environment setup / Inference / Training / Evaluation` 均 `Coming Soon`
  - 因此从当前项目依赖中移除，不再作为 baseline blocker 或 acquisition gate

## Process Blockers

- `baseline_repo_registry_v1` 已补 `MLD` host-level 记录，但 standalone canonical repo 仍不存在。
- `baseline_readiness_manifest_v1 / dataset_readiness_manifest_v1 / smoke_logs_v1` 已创建，但还需要后续 agent 持续更新，而不是一次性扫描后停止。

### Route-A learned grounding 候选审计（2026-04-24 修订）

Route-A 当前已不再把 ZOMG / TM-Mamba / TMR 记为 current-cycle 执行依赖（见 exec §5.1.1、localizer §1-2）。审计结论：

- note:
  - `ZOMG` 当前只有占位仓库，不能视作可运行开源实现
  - `TM-Mamba` 未核到官方公开代码/权重
  - 因此当前 Route-A 冻结为 rule-first coarse checker，不再把 `TMR / ZOMG` 记成 P3 资产 blocker
- effect:
  - 当前周期的 P3 blocker 不在 `TMR / ZOMG` 资产，而在主线 stop note 与后续 audit/threshold 校准

### Mainline Interface Chain (2026-04-24)

- blocked segment:
  - `canonical_22j -> MotionFix pose(135)`
- already verified:
  - `Event-T2M raw 263 -> canonical_22j(+root)` extraction 已通过，见 `[[artifacts/modebug/eventt2m_adapter_smoke/modebug_eventt2m_adapter_smoke_report.json]]`
  - `MotionFix` 本地 checkpoint / evaluator / dataset / body models 在位，不是当前主 blocker
- concrete blockers:
  - `Event-T2M` 的 `visualize/utils/simplify_loc2rot.py` 默认依赖 repo-local `visual_datas/render_deps/`，但当前 repo 中该目录缺失；要跑 `joints2smpl` 必须 runtime remap 到现有 `SMPL` assets 与 `neutral_smpl_mean_params.h5`
  - `Event-T2M` 与 `motionfix` 都占用顶层 `src` 包名；bridge 需要显式隔离 import order / env path，不能直接把两个 repo 当单一 package 混用
  - 当前 repo 工具链不提供 import-ready 的 strict `generated T x 22 x 3 -> same T x 263` 逆映射；`process_file()` 依赖未初始化全局量，且 HumanML3D feature builder 会折叠一个 terminal frame
- effect:
  - 主线 P0 smoke 目前只通过了 Gate 1；Gate 2 未闭合前，不进入 `fair matrix -> failure map -> localizer -> repair`
