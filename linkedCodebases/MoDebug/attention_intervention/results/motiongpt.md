# MotionGPT Attention Intervention 报告

## 状态

| 项目 | 值 |
|---|---|
| Baseline | MotionGPT |
| 架构 | 12 个 T5 decoder layer |
| 已完成 families | baseline, SA, CA |
| Unsupported families | CFG_SA, CFG_CA |
| Formal run roots | `motiongpt/formal_candidates/trace1_full_eval_*_20260605_*` |
| 已完成 manifests | 25 个 full evaluator results |
| 中位运行时间 | 单层约 3.8 min |

CFG_SA 和 CFG_CA 不计为缺失实验。MotionGPT wrapper 已用 `paper_level_status: unsupported_family_fail_fast` 明确阻断。

## 审计证据

| 证据 | 状态 | 说明 |
|---|---:|---|
| `paper_level_status` | OK | Baseline、SA、CA formal manifests 均为 `full_evaluator_metrics_computed`。 |
| Metrics files | OK | `metrics_summary.json` 存在且非空。 |
| Provenance | OK | Manifests 包含 command script、wrapper script、checkpoint hashes、git head/status、layer mapping、supported/unsupported family lists。 |
| Hook evidence | OK | 支持的 families 包含 hook call counts 和 replacement check fields。 |
| Unsupported CFG handling | OK | CFG_SA 和 CFG_CA 均有 fail-fast preflight manifests。 |

远程 roots：

```text
/data/public/ripemangobox/Motion/experiments/MoDebug/motiongpt/formal_candidates
/data/public/ripemangobox/Motion/experiments/MoDebug/motiongpt/preflight/failfast_cfg_sa_20260605_v3
/data/public/ripemangobox/Motion/experiments/MoDebug/motiongpt/preflight/failfast_cfg_ca_20260605_v3
```

## 指标汇总

指标来自 MotionGPT official evaluator。同一 baseline 内，FID、Matching 越低越好；Top1/Top2/Top3、Diversity、MultiModality 通常越高越好。Top1/Top2/Top3 均来自原始 `metrics_summary.json`，不是事后估算。

| Family | N | FID mean | Best FID | Best FID layer | Top1 mean | Top2 mean | Top3 mean | Best Top1 | Best Top1 layer | Best Top2 | Best Top2 layer | Best Top3 | Best Top3 layer | Matching mean | Diversity mean | MultiModality mean | Median min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 1 | 0.1945 | 0.1945 | NA | 0.3991 | 0.5724 | 0.6565 | 0.3991 | NA | 0.5724 | NA | 0.6565 | NA | 4.0338 | 9.4327 | 3.4791 | 3.98 |
| SA | 12 | 0.2013 | 0.1708 | 8 | 0.4068 | 0.5731 | 0.6635 | 0.4155 | 6 | 0.5864 | 6 | 0.6718 | 3 | 3.9898 | 9.2320 | 3.4513 | 3.82 |
| CA | 12 | 0.1954 | 0.1687 | 9 | 0.4041 | 0.5675 | 0.6580 | 0.4164 | 0 | 0.5780 | 0 | 0.6651 | 0 | 4.0390 | 9.2370 | 3.6001 | 3.82 |

## 层趋势视图

![MotionGPT FID layer trend](../visualization/figures/motiongpt_fid.svg)

![MotionGPT Top1 layer trend](../visualization/figures/motiongpt_top1.svg)

![MotionGPT Top2 layer trend](../visualization/figures/motiongpt_top2.svg)

![MotionGPT Top3 layer trend](../visualization/figures/motiongpt_top3.svg)

FID trend，越低越好：

```text
SA 00:.233 01:.192 02:.184 03:.215 04:.183 05:.197 06:.193 07:.244 08:.171 09:.197 10:.210 11:.198
CA 00:.228 01:.171 02:.192 03:.181 04:.221 05:.209 06:.188 07:.175 08:.208 09:.169 10:.235 11:.169
```

Top3 trend，越高越好：

```text
SA 00:.660 01:.663 02:.661 03:.672 04:.666 05:.648 06:.670 07:.666 08:.657 09:.666 10:.669 11:.664
CA 00:.665 01:.664 02:.663 03:.660 04:.653 05:.658 06:.661 07:.661 08:.659 09:.657 10:.647 11:.647
```

## Unsupported CFG Families

| Family | 状态 | 原因 |
|---|---|---|
| CFG_SA | `unsupported_family_fail_fast` | MotionGPT wrapper 没有暴露该 intervention 定义所需的 paired unconditional CFG branch。 |
| CFG_CA | `unsupported_family_fail_fast` | 同样受 CFG branch 限制；CA-only intervention 已支持并完成。 |

## 解读备注

- MotionGPT 是三套 baseline 中最快的一个，formal 单层约 3.8 分钟。
- 支持的 SA/CA intervention 相对 baseline 没有明显 aggregate metric shift。
- 除非重新设计并审查 MotionGPT-specific CFG 定义，否则 CFG families 应继续标记为 unsupported。
