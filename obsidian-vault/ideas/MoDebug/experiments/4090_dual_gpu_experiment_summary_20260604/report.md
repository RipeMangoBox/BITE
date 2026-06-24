---
title: "4090 双卡实验结果整理"
created: 2026-06-04T13:09:00+08:00
updated: 2026-06-04T13:39:26+08:00
status: summarized
tags:
  - MoDebug
  - experiments
  - MotionCLR
  - MoLingo
  - Trace1
  - Trace3
---

# 4090 双卡实验结果整理

生成时间：2026-06-04 Asia/Shanghai  
本地目录：`obsidian-vault/ideas/MoDebug/experiments/4090_dual_gpu_experiment_summary_20260604/`

## 总览

截至 2026-06-04 13:09 CST，4090 两张卡都空闲，GPU0/GPU1 均无 compute 进程；tmux 里只看到 TensorBoard 会话，没有训练或 eval 会话在继续推进。

这轮双卡主要对应两个 idea 方向：

| GPU | 最近实验 | idea / trace | 状态 | 结论边界 |
|---:|---|---|---|---|
| 0 | MotionCLR `trace3_formal_train_ds_review_20260603_gpu0` | Trace 3 / Line 3 / old Track A | `baseline`、`disploss`、`aug_disploss` 完成 50k step；`aug` 中断 | 只有训练与 reconstruction proxy；仍需 official evaluator |
| 1 | MoLingo `molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1` | Trace 1 layer/attention intervention diagnostic | 完成，`failures=[]` | layer sweep 诊断，不是最终 paper-level evaluator |
| 1 | MotionCLR `trace1_formal_layer_sweep_ds_review_20260603_gpu1` | Trace 1 / Line 1 / old Track B | 同日更早完成 | layer sweep 诊断，不是最终 paper-level evaluator |

本地已整理出 raw JSON/log、CSV 表格、SVG 图表和机器可读汇总：`summary_data.json`。

## GPU0: MotionCLR Trace3

远端根路径：

`/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0`

Trace3 是训练候选实验，不是最终评测结果。manifest 中 `paper_level_status=not_final_until_official_evaluator_metrics` 且 `official_eval_required_after_training=true`。

| variant | 状态 | steps | 耗时 h | train tail1000 | val proxy last | eval proxy last | 备注 |
|---|---:|---:|---:|---:|---:|---:|---|
| `baseline` | completed | 50000 | 5.033 | 0.315566 |  |  | 无 val/eval proxy，是最早完成的训练 |
| `disploss` | completed | 50000 | 5.040 | 0.322711 | 0.322431 | 0.310036 | 有 100 次 val、20 次 eval proxy |
| `aug_disploss` | completed | 50000 | 5.162 | 0.324350 | 0.323705 | 0.310575 | aug cumulative rate = 0.282074 |
| `aug` | interrupted | 约 4.6k TB scalar |  |  |  |  | 无 manifest/loss_steps/val/eval，不作为完成结果 |

Proxy best 指标：

| variant        | split | points | best loss | best step | last loss |
| -------------- | ----- | -----: | --------: | --------: | --------: |
| `disploss`     | val   |    100 |  0.272567 |     48500 |  0.322431 |
| `disploss`     | eval  |     20 |  0.294936 |     37500 |  0.310036 |
| `aug_disploss` | val   |    100 |  0.271674 |     48500 |  0.323705 |
| `aug_disploss` | eval  |     20 |  0.299013 |     37500 |  0.310575 |

训练曲线里存在早期异常大 outlier；图中使用每个 variant 的 p99 裁剪后 rolling mean，原始 outlier 已写入 `tables/motionclr_trace3_train_loss_outliers.csv`。

![[figures/motionclr_trace3_train_loss_rolling.svg]]

![[figures/motionclr_trace3_val_loss.svg]]

![[figures/motionclr_trace3_eval_loss.svg]]

![[figures/motionclr_trace3_final_proxy_bar.svg]]

![[figures/motionclr_trace3_disp_loss_rolling.svg]]

![[figures/motionclr_trace3_aug_rate.svg]]

初步读法：`disploss` 和 `aug_disploss` 在 proxy val 上非常接近，`aug_disploss` 的 best val 略低，但 eval proxy 略差；这些差异不足以替代 official evaluator。下一步应运行已经准备好的 official ckpt 对比 eval。

## GPU1: MotionCLR Trace1

远端根路径：

`/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_formal_layer_sweep_ds_review_20260603_gpu1`

配置：64 prompts，seeds `[0,1,2]`，18 layers，耗时约 0.146 h，`failures=0`。这是 MotionCLR 上的 Trace1 layer sweep 诊断。

Family 级 L2 差异：

| family                   | rows |  L2 mean |   L2 max |   L2 min |
| ------------------------ | ---: | -------: | -------: | -------: |
| `noop`                   |    6 |    0.000 |    0.000 |    0.000 |
| `ca_output_perturbation` |   54 |  524.498 | 1510.484 |   52.824 |
| `cfg_hidden_replacement` |   54 |  993.251 | 2627.410 |  136.169 |
| `positive_control`       |    6 | 2608.902 | 2627.410 | 2592.416 |

Layer 趋势：MotionCLR 的 hidden replacement 在后段更强，L15 hidden mean L2 约 2608.90，L14 hidden 约 2431.20；CA perturbation 在 L0、L12 附近更强。

![[figures/motionclr_trace1_family_l2_mean.svg]]

![[figures/motionclr_trace1_layer_l2_heatmap.svg]]

![[figures/motionclr_trace1_top_layer_l2.svg]]

## GPU1: MoLingo Trace1

远端根路径：

`/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1`

配置：64 prompts，seeds `[0,1,2]`，16 layers，耗时约 10.986 h，`failures=0`。这是 GPU1 最近一次主运行。

Family 级 L2 差异：

| family                   | rows |  L2 mean |   L2 max |   L2 min |
| ------------------------ | ---: | -------: | -------: | -------: |
| `noop`                   |    6 |    0.000 |    0.000 |    0.000 |
| `ca_output_perturbation` |   48 | 1185.511 | 1615.762 |  813.314 |
| `cfg_hidden_replacement` |   48 | 2158.660 | 3360.816 |  856.525 |
| `positive_control`       |    6 | 3306.222 | 3487.929 | 3173.838 |

Layer 趋势：MoLingo 的 hidden replacement 后层效应最强，L15 hidden mean L2 约 3260.63，L14 hidden 约 2609.66，L13 hidden 约 2520.47。CA perturbation 中 L10 最高，mean L2 约 1548.25。

![[figures/molingo_trace1_family_l2_mean.svg]]

![[figures/molingo_trace1_layer_l2_heatmap.svg]]

![[figures/molingo_trace1_top_layer_l2.svg]]

## 跨模型观察

Trace1 在 MotionCLR 和 MoLingo 上都通过了基本 sanity：`noop` 为 0，positive control 明显非零。两个模型都显示 hidden replacement 的影响通常强于 CA output perturbation；MoLingo 的绝对 L2 差异整体更大，且后层 hidden replacement 的相对趋势更单调。

![[figures/trace1_cross_model_relative_depth_profile.svg]]

这个跨模型图按各自 family 的最大 L2 做归一化，只用于比较层深趋势，不用于比较模型绝对优劣。

## 本地文件索引

关键文件：

- `raw_remote/`: 远端 JSON/log/prompt/manifest 的本地快照。
- `tables/experiment_status.csv`: 实验身份、trace、GPU、耗时、状态总表。
- `tables/motionclr_trace3_variant_summary.csv`: Trace3 三个完成 variant 的核心训练/proxy 指标。
- `tables/motionclr_trace3_proxy_best.csv`: Trace3 val/eval proxy best step。
- `tables/motionclr_trace3_train_loss_outliers.csv`: 训练曲线 outlier 与裁剪阈值。
- `tables/motionclr_trace1_*`: MotionCLR Trace1 layer sweep 明细与聚合。
- `tables/molingo_trace1_*`: MoLingo Trace1 layer sweep 明细与聚合。
- `figures/`: 所有 SVG 图表。
- `summary_data.json`: 机器可读聚合摘要。

## 后续建议

1. 对 GPU0 的 `baseline`、`disploss`、`aug_disploss` 跑 official evaluator，并与 official ckpt 做同协议对比。
2. `aug` 单独 variant 当前只有中断日志，不建议纳入结论；如果仍关心 pure augmentation，需要按现在的 val/eval interval 重跑。
3. Trace1 的 layer sweep 可以作为机制诊断证据，但不能替代 FID/R-precision/matching score/diversity 等正式指标。
4. 当前未观察到自动继续启动训练/eval 的 tmux；只有 TensorBoard 会话仍在。






要求:
  1. 操作定义：
	  1. CA扰动：只对cross attention layer的hidden layer进行适度扰动；
	  2. SA扰动：只对self attention layer的hidden layer进行适度扰动；
	  3. CFG_CA或CFG_SA：按照official ckpt的cfg weight，每次只对一层CA或SA使用对应 uncond 的 hidden feature 替换，其他
	  4. 
  2. 原本的CA和CFG_CA仅对L2的loss进行捕捉.请在GPU0重新完成CA扰动和CFG_CA实验,除了l2 loss,还需要进行完整的eval（首先多agent确认每个baseline仓库的eval脚本是否能完整计算paper涉及的metrics,如果缺失重大请提前告知）;
  3. GPU1进行与GPU0对应的SA扰动和CFG_SA的实验
  4. 所有代码都需要经过ds严格审查敲定才能执行。
  5. 所有数据通过正式实验获得，不能通过smoke伪造
  6. 预估两张卡的bash串行各自的完成时间