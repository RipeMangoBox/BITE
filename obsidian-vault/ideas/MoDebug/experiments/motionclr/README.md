---
title: "MotionCLR Experiments"
created: 2026-06-03T16:45:02+08:00
updated: 2026-06-14T00:00:00+08:00
status: active
tags:
  - MoDebug
  - motionclr
  - experiments
---

# MotionCLR Experiments

## 当前入口

| 文件夹或文件 | 角色 |
|--------------|------|
| [[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]] | Trace 1 formal diagnostic 数据分析、折线图和结论边界。 |
| [[experiments/archived/v2/motionclr/2026-06-02_ds_formal_experiment_gate]] | MotionCLR Trace 1/3 DS gate 与正式候选边界。 |
| [[experiments/archived/v2/motionclr/2026-06-02_dual_trace_bounded_validation_status]] | 早期 bounded validation，已被 formal run 取代。 |
| [[experiments/archived/v2/motionclr/2026-06-02_dual_trace_supervision]] | 旧监督记录，当前只保留历史边界。 |
| `scripts/` | MotionCLR 专属实验脚本。 |
| `commands/` | MotionCLR 专属远端运行命令。 |

## 远端根目录

`/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/`

## 状态

- Trace 1 formal diagnostic layer sweep 已完成；图和结论见 [[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。
- Trace 3 formal candidate real training 已整理到 [[../4090_dual_gpu_experiment_summary_20260604/report]]；official evaluator 未完成前不写 paper-level 指标。
- Trace 1 full official evaluator 已通过 DS 二次 gate、两个补充 preflight 和 DS 中途严审；GPU0/GPU1 正式串行运行已于 2026-06-04T15:13+08:00 启动。

## Trace 1 full evaluator 准备项

| 文件 | 角色 |
|------|------|
| `scripts/trace1_full_eval_attention_intervention.py` | 基于 MotionCLR official evaluator 的 full metric wrapper；不修改 MotionCLR repo 源码。 |
| `commands/trace1_full_eval_gpu0_ca_cfg_ca_command.sh` | GPU0 串行运行 baseline、逐层 CA 扰动、逐层 CFG_CA。 |
| `commands/trace1_full_eval_gpu1_sa_cfg_sa_command.sh` | GPU1 串行运行 baseline、逐层 SA 扰动、逐层 CFG_SA。 |

> [!warning] CFG_CA 定义边界
> MotionCLR 的 uncond 分支不调用 `CrossAttention`，因此不能替换“uncond CA output”。本轮 CFG_CA 按 DS 批准的边界定义实现：在指定层 self-attention 后保存 `pre_ca`，执行 cond 分支 CA 后，用 uncond 分支的 post-self-attention/pre-CA hidden 替换 cond 分支 post-CA hidden。报告中必须标注为 `cfg_ca_boundary_hidden_replacement`。
> 实现上只会在 CFG_CA variant 内临时 patch 目标层实例的 `ResidualCLRAttentionLayer.forward`；非目标层保持原始 forward。早期 `cfg_ca/layer_0` 和 `cfg_ca/layer_1` manifest 的 limitation 文案若写成 shared method patch，应按本段纠正解释。

## Trace 1 DS 二次 gate

- DS 判决：`APPROVE_AFTER_SMALL_PREFLIGHT`；要求正式长跑前补 `CFG_SA layer1` 与 `CFG_CA layer5` 轻量预检。
- 预检结果：
  - `trace1_full_eval_ds_required_cfg_sa_layer1_20260604_gpu1_r2`: `failures=[]`, hook `{1: 236}`, replacement checks `236`, `max_before_max=3.400174140930176`, `max_after_max=0.0`。
  - `trace1_full_eval_ds_required_cfg_ca_layer5_20260604_gpu0_r2`: `failures=[]`, hook `{5: 236}`, replacement checks `236`, `before_max=15.980764389038086`, `after_max=0.0`。
- 原 layer0 preflight 通过，但 `CFG_SA layer0` 为 no-op；原因是 layer0 self-attention 位于任何 conditional CA 之前，CFG combined batch 的 cond/uncond 输入完全相同。layer1 补充预检已确认 CFG_SA 进入非零替换。

## 正式运行状态

远端运行根目录：

- GPU0: `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_full_eval_ca_cfg_ca_ds_review_20260604_gpu0`
- GPU1: `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260604_gpu1`

tmux:

- `modebug_trace1_full_gpu0_ca_cfg_ca_20260604`
- `modebug_trace1_full_gpu1_sa_cfg_sa_20260604`

远端 tee 日志：

- `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug_trace1_full_gpu0_ca_cfg_ca_20260604.log`
- `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug_trace1_full_gpu1_sa_cfg_sa_20260604.log`

参数：`NUM_INFERENCE_STEPS=10`, `REPLICATION_TIMES=1`, `BATCH_SIZE=32`, layers `0..17`，每个 variant 单层运行；已有 `manifest.json` 会被跳过。

截至 2026-06-04T15:39+08:00：

- GPU0 已落盘 3 个正式 manifest：`baseline`, `ca/layer_0`, `cfg_ca/layer_0`；tmux 继续运行到 `ca/layer_1`。
- GPU1 已落盘 3 个正式 manifest：`baseline`, `sa/layer_0`, `cfg_sa/layer_0`；tmux 继续运行到 `sa/layer_1`。
- DS 中途判决：`CONTINUE`。`2360` hook calls 符合 `236` batches × `10` diffusion steps。
- `cfg_sa/layer_0` 正式结果与 baseline 完全一致，这是预期 no-op：layer 0 self-attention 位于任何 conditional CA 前，cond/uncond hidden 相同。最终分析必须保留此点，不能当作实现失败，也不能作为深层 CFG_SA 结果的替代证据。
- `cfg_ca/layer_0` replacement checks 为 `2360`，before 非零、after 为 `0.0`；最终分析必须继续标注为 `cfg_ca_boundary_hidden_replacement`，不能描述成 true uncond CA output replacement。

截至 2026-06-04T15:51:13+08:00：

- DS 批准 metadata-only patch：`APPROVE_SYNC`。该补丁不改变干预张量计算、生成、evaluation 调用或命令脚本，只补 manifest provenance/config 字段并修正 CFG_CA limitation 文案。
- wrapper 已同步到 4090：`/data/public/ripemangobox/Motion/experiments/MoDebug/scripts/trace1_full_eval_attention_intervention.py`，sha256 `4d25cf4af5699aff95447dffd3ec4775799d5ba0044533840e4add630fddf960`。
- 远端命令脚本 hash：GPU0 `eb15d6f8146359ea12c49177ed14e2add7222eb0fc964aab40100b5d924acfef`；GPU1 `1f0ce2fb5cee0c24989bbcfad2f4f5724aacf22ed3d6811dbb742db4c881f125`。
- 已落盘或已经启动的早期 variants 仍可能缺少 `wrapper_script`, `command_script`, `config_files`, `eval_protocol` 等新增 manifest 字段。不要把这些缺字段误判为实验无效；最终验收需区分 metadata patch 前后。
- 因同步时 `ca/layer_2` 和 `sa/layer_2` 的 Python 进程已经启动，新增 manifest 字段预计从随后启动的 `cfg_ca/layer_2` 和 `cfg_sa/layer_2` 或更晚 variants 开始出现。

## 预计耗时

单个 full evaluator variant 预计约 35-60 分钟。因为用户要求“每次只对一层”，GPU0 需要 baseline + 18 层 CA + 18 层 CFG_CA，GPU1 需要 baseline + 18 层 SA + 18 层 CFG_SA；`replication_times=1` 时每张卡预计约 21-37 小时。若提高 replication，耗时近似线性增加。
