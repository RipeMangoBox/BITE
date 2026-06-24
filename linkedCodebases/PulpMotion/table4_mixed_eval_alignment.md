# PulpMotion Table 4 Mixed Eval 对照

生成时间：2026-06-08

## 结论

本次真实完成的是 mixed subset 上的 `DiT (x, y)+Aux` 与 `MAR (x, y)+Aux` 单次 eval，使用 `seed=42`、`batch_size=16`。它对应论文 Table 4 中 DiT/MAR 段落里最终的 `(x, y)+Aux (ours)` 行。

这些结果是单次 sanity eval，不是论文中的 10 samplings 95% CI。

## Table 4 口径对照

| Methods | Source | FD_framing ↓ | Out-rate ↓ | FD_TMR ↓ | TMR-Score ↑ | Coverage ↑ | FD_CLaTr ↓ | CLaTr-Score ↑ | F1 ↑ | Coverage ↑ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DiT `(x, y)+Aux (ours)` | Paper Table 4 | 3.37±0.02 | 16.76±0.19 | 431.54±1.15 | 25.05±0.07 | 8.91±0.13 | 80.08±0.76 | 32.81±0.19 | 36.06±0.25 | 48.68±0.20 |
| DiT `(x, y)+Aux (ours)` | Re-run, seed 42, bs16 | 3.93 | 18.31 | 426.26 | 24.92 | 8.62 | 79.84 | 33.52 | 36.79 | 49.02 |
| MAR `(x, y)+Aux (ours)` | Paper Table 4 | 6.42±0.04 | 33.65±0.23 | 301.39±0.25 | 24.46±0.07 | 14.14±0.14 | 108.74±0.46 | 45.96±0.14 | 45.39±0.22 | 53.67±0.38 |
| MAR `(x, y)+Aux (ours)` | Re-run, seed 42, bs16 | 6.37 | 35.79 | 295.88 | 23.51 | 16.09 | 112.01 | 41.71 | 42.10 | 55.24 |

## Metric key 映射

| Table 4 column | 当前 eval key | 表格显示换算 | 说明 |
|---|---|---:|---|
| `FD_framing ↓` | `projection/r_fpd` | raw | repo 中命名为 projection relative FPD；对应 framing FD。 |
| `Out-rate ↓` | `projection/outscreen` | `value * 100` | 当前输出是 0-1 比例，Table 4 显示百分数。 |
| `FD_TMR ↓` | `tmr/ftd` | raw | TMR feature Frechet distance。 |
| `TMR-Score ↑` | `tmr/tmr_score` | raw | cosine similarity score，代码内部已乘 100。 |
| Human `Coverage ↑` | `tmr/coverage` | `value * 100` | PRDC coverage。 |
| `FD_CLaTr ↓` | `clatr/fcd` | raw | CLaTr feature Frechet distance。 |
| `CLaTr-Score ↑` | `clatr/clatr_score` | raw | cosine similarity score，代码内部已乘 100。 |
| `F1 ↑` | `captions/f1` | `value * 100` | camera segment/caption F1。 |
| Camera `Coverage ↑` | `clatr/coverage` | `value * 100` | PRDC coverage。 |

## 当前 eval 实际打印的完整 key

本次成功日志中 `src/evaluate.py` 最终 `print(metrics_dict)` 打印了以下 key，并已解析写入远端 JSON：

```text
captions/f1
captions/precision
captions/recall
clatr/clatr_score
clatr/coverage
clatr/density
clatr/fcd
clatr/precision
clatr/recall
projection/coverage
projection/density
projection/g_fpd
projection/outscreen
projection/precision
projection/r_fpd
projection/recall
tmr/R1
tmr/R2
tmr/R3
tmr/coverage
tmr/density
tmr/ftd
tmr/precision
tmr/recall
tmr/tmr_score
```

Table 4 可比较主列需要的指标都在这些打印 key 中。这里没有列出 `R3`，因为当前官方 eval 的 retrieval metric 是在 dataloader batch 内计算，本次成功运行的 `batch_size=16` 会显著影响该值；若要严格对照论文 `R3`，需要改为全 test set feature 汇总后统一计算 retrieval。

## 是否记录了 print 以外的 metric

结论：当前实验 artifact 中没有可用的、比最终 `print(metrics_dict)` 更多的 metric 记录。

代码层面确实还有一些 callback 会计算或返回额外字段，但 `src/evaluate.py` 没有把它们写入最终 `metrics_dict`，本次日志和 JSON 里也没有保存它们：

| 内部字段 | 状态 | 说明 |
|---|---|---|
| `test/proj/error` | callback 计算，但 `evaluate.py` 未打印 | `JointMetricCallback.compute_joint_metrics()` 返回该字段；最终 `metrics_dict` 没收集。 |
| `test/tmr/mm_distance` | retrieval callback 返回，但 `evaluate.py` 未打印 | `RetrievalMetric.compute()` 返回 `mm_distance`；最终只取了 `R1/R2/R3`。 |
| `test/clatr/R1/R2/R3` | camera retrieval callback 返回，但 `evaluate.py` 未打印 | 当前 Table 4 不需要 CLaTr retrieval R 值。 |
| `test/clatr/mm_distance` | retrieval callback 返回，但 `evaluate.py` 未打印 | 同上。 |

这些字段在当前已结束 run 中无法从现有 log post-hoc 恢复。若后续确实需要，建议做一个最小 wrapper 或补丁，在 `trainer.test(...)` 后把 `model.eval_metrics` 全量序列化为 JSON；这比解析 stdout 更可靠。

## Artifact 路径

远端结果目录：

```text
/data/public/ripemangobox/Motion/PulpMotion/artifacts/eval_runs/pulpmotion_paper_aux_20260608
```

关键文件：

```text
mixed_dit_aux_bs16.metrics.json
mixed_mar_aux_bs16.metrics.json
mixed_aux_bs16.summary.json
mixed_aux_bs16.summary.md
mixed_dit_aux_bs16_gpu0.log
mixed_mar_aux_bs16_gpu1.log
```
