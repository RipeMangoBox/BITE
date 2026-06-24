---
title: "Cross-Baseline CA CFG Gate"
created: 2026-06-03T16:45:02+08:00
updated: 2026-06-03T18:16:00+08:00
status: molingo_formal_running
tags:
  - MoDebug
  - trace_1
  - baseline_gate
  - ds-review
---

# Cross-Baseline CA CFG Gate

> [!abstract] DS 门禁结论
> 本轮只批准 MoLingo 进入 GPU1 串行 Trace 1 CA/CFG formal diagnostic candidate。MotionGPT、MotionStreamer、MotionAgent 均不进入本轮运行。

## 判定

| Baseline | 4090 repo | CA | CFG official setting | DS verdict | 处理 |
|----------|-----------|----|----------------------|------------|------|
| MotionCLR | `/data/public/ripemangobox/Motion/MotionCLR` | yes | cfg scale 2.5 | completed | 已完成，见 [[motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。 |
| MoLingo | `/data/public/ripemangobox/Motion/MoLingo` | yes | README demo / opt: `cfg=4.0`, `step=32`, `acc=1` | `APPROVE` | v4 dev validation 已通过；formal diagnostic 正在 GPU1 运行。 |
| MotionGPT | `/data/public/ripemangobox/Motion/MotionGPT` | T5 encoder-decoder CA exists | no classifier-free guidance scale in README; `--cfg` is config path | `BLOCK` | 不跑本轮 CA+CFG。 |
| MotionStreamer | `/data/public/ripemangobox/Motion/MotionStreamer` | no cross-attention; causal self-attention only | code default CFG 4.0 | `BLOCK` | 不跑本轮 CA 诊断。 |
| MotionAgent | not found locally | not applicable | not applicable | `BLOCK` | 本地无 repo，且是 video I2V domain。 |

## MoLingo 执行边界

- baseline: MoLingo 272D official generation path。
- runtime env: 4090 上没有 `environment.yml` 中的 `molingo` env；`event-t2m` 已通过 MoLingo import smoke，实际 dev/formal run 使用 `event-t2m`。
- official setting: `cfg=4.0`、`step=32`、`acc=1`。`acc=1` 来自 README demo 显式 `-a 1`，而不是 argparse default `acc=3`。
- CA hook: `MoLingo.seqTransDecoder.layers[i].multihead_attn` output suppression。
- CFG hidden replacement: 每个 sampling step 先缓存 force-mask uncond 分支在指定 decoder layer 的 hidden output，再在 cond 分支同层替换为该 uncond hidden，之后继续原始 CFG mixing。
- 输出指标仅为 decoded normalized 272D feature array 相对 baseline 的 L2、mean abs、max abs。
- 不报告 FID、R-Precision 或 paper-level performance。

## Dev Validation

- run: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/dev_validation/molingo_trace1_formal_layer_sweep_dev_20260603_gpu1_v4/`。
- log: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_trace1_dev_20260603_gpu1_v4.log`。
- result: `failures=[]`，elapsed `308.0s`，env `event-t2m`，device `CUDA_VISIBLE_DEVICES=1`。
- no-op controls: `noop_ca_all_layers_alpha_1` 与 `noop_hidden_hook_all_layers_disabled` 均 `allclose=True`，`l2=0.0`。
- positive controls: `positive_control_ca_all_layers_alpha_0p0` 的 `l2=827.6823`，`positive_control_hidden_replace_all_layers` 的 `l2=816.5783`，均 `allclose=False`。
- dev layers: layer 0 与 layer 15 的 CA output suppression 和 CFG hidden replacement 均产生非零扰动。
- prompt guard: formal 脚本已加入 `--prompt_count_min`，防止 prompt 文件少于目标数量时静默继续。

## Formal Run

- tmux: `modebug_molingo_trace1_formal_test64_20260603`。
- log: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_trace1_formal_test64_20260603_gpu1.log`。
- prompt set: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt`，从 272D HumanML3D test split 固定抽取 64 条 caption。
- output: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1/`。
- scope: 64 prompts × 3 seeds × 16 decoder layers × 2 perturbation families, plus baseline/no-op/positive controls.
- aborted run: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_ds_review_20260603_gpu1/` 只用了 MoLingo demo `assets/example.txt` 的 10 条 prompt，已停止，不纳入正式结论。

## Serial Supervisor

- tmux: `modebug_serial_supervisor_20260603`。
- log: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug_serial_supervisor_20260603.log`。
- script: `/data/public/ripemangobox/Motion/experiments/MoDebug/commands/modebug_serial_supervisor_4090.sh`。
- behavior: 等待 MoLingo test64 formal manifest 并校验 `failures=[]` / `num_prompts>=64`；随后等待 MotionCLR Trace3 training 四个 manifest；最后串行执行 Trace3 official eval。

## 下一步

1. 优先监控 serial supervisor log；它负责等待和触发后续步骤。
2. MoLingo formal 完成且 `failures=[]` 后，绘制 MoLingo 折线图，并与 MotionCLR 分开放在 baseline 目录下。
3. formal summary 完成前，不写 MoLingo CA/CFG 的正式层级结论。
