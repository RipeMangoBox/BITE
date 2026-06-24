# MoLingo Attention Intervention 报告

## 状态

| 项目 | 值 |
|---|---|
| Baseline | MoLingo |
| 架构 | 16 个 TransformerDecoder layer |
| 状态 | 20260609 official-setting 代表层重跑完成 |
| 旧结果处理 | 20260603/20260605 旧 eval 作废并从 active `formal_candidates` 删除 |
| 代表层 | `5,10,15` |
| 双路线 | GPU0: baseline + CA + CFG_CA；GPU1: SA + CFG_SA |
| 完成项 | baseline + SA/CA/CFG_SA/CFG_CA representative layers |

远程 active roots：

```text
/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/trace1_full_eval_ca_cfg_ca_official_20260609_gpu0
/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/trace1_full_eval_sa_cfg_sa_official_20260609_gpu1
```

## 作废原因

20260603/20260605 MoLingo eval 不再作为正式结果使用，原因如下：

| 问题 | 影响 |
|---|---|
| `Text2MotionDatasetMS` 的 `unit_length` 被硬编码为 `4` | 与 MoLingo official `eval_mogen.py` 的 `int(2 ** vae_opt.down_t)` 不一致；该 VAE `down_t=1`，official 值应为 `2`。 |
| 命令使用 `cfg=4.0, acc=5` | 与 official 默认 `cfg=5.5, acc=3` 不一致。 |
| manifests 缺少 hook/replacement 运行时证据 | CFG_SA/CFG_CA 只能做代码级推断，不能满足正式审计要求。 |

远端保留作废记录：

```text
/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/invalidated_20260609/invalidation_manifest.json
```

## Official-setting 重跑设置

runner 修复：

- `unit_length` 从 VAE `down_t` 动态计算，并写入 manifest。
- `eval_settings` 记录 `cfg=5.5`、`acc=3`、`sample_steps=32`、`repeat=1`、`unit_length`、`vae_down_t`。
- manifest 记录 model/VAE `opt` 和 checkpoint hash。
- SA/CA 写 `hook_call_counts.scale_hook`；CFG_SA/CFG_CA 写 `forward_with_cfg`、`capture_hook`、`replace_hook` 和 replacement checks。
- 非 baseline 干预若 hook/replacement 未触发，manifest 置为 failed，不静默产出 full evaluator。

启动命令：

```text
BASELINES=molingo RUN_DATE=20260609 LAYERS_16=5,10,15 \
  bash /data/public/ripemangobox/Motion/experiments/MoDebug/commands/run_three_baselines_serial_dual_gpu.sh
```

## 指标汇总

指标来自 MoLingo official MS evaluator。FID_TMR 越低越好；Top1/Top2/Top3 越高越好。

| Family | N | FID_TMR mean | Best FID_TMR | Best FID layer | Top1 mean | Top2 mean | Top3 mean | Best Top1 | Best Top1 layer | Matching mean | 状态 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| baseline | 1 | 3.5944 | 3.5944 | NA | 0.7755 | 0.9026 | 0.9402 | 0.7755 | NA | 14.7401 | complete |
| SA | 3 | 3.8398 | 3.5085 | 5 | 0.7785 | 0.9027 | 0.9434 | 0.7819 | 10 | 14.6909 | complete |
| CA | 3 | 3.7344 | 3.6528 | 10 | 0.7716 | 0.9018 | 0.9414 | 0.7749 | 10 | 14.8140 | complete |
| CFG_SA | 3 | 3.9634 | 3.5982 | 5 | 0.7735 | 0.8988 | 0.9402 | 0.7771 | 10 | 14.7370 | complete |
| CFG_CA | 3 | 5.0345 | 3.6466 | 10 | 0.7557 | 0.8901 | 0.9328 | 0.7755 | 5 | 15.0724 | complete |

Layer metrics：

| Family | Layer | FID_TMR | Top1 | Top2 | Top3 | Matching |
|---|---:|---:|---:|---:|---:|---:|
| CA | 5 | 3.6773 | 0.7724 | 0.9031 | 0.9432 | 14.7253 |
| CA | 10 | 3.6528 | 0.7749 | 0.9062 | 0.9446 | 14.7095 |
| CA | 15 | 3.8732 | 0.7676 | 0.8962 | 0.9364 | 15.0071 |
| CFG_CA | 5 | 3.7566 | 0.7755 | 0.9001 | 0.9400 | 14.7220 |
| CFG_CA | 10 | 3.6466 | 0.7676 | 0.9010 | 0.9418 | 14.7573 |
| CFG_CA | 15 | 7.7003 | 0.7240 | 0.8691 | 0.9165 | 15.7381 |
| SA | 5 | 3.5085 | 0.7755 | 0.9026 | 0.9411 | 14.7585 |
| SA | 10 | 3.5621 | 0.7819 | 0.9021 | 0.9453 | 14.6852 |
| SA | 15 | 4.4487 | 0.7781 | 0.9033 | 0.9439 | 14.6290 |
| CFG_SA | 5 | 3.5982 | 0.7760 | 0.9008 | 0.9407 | 14.7316 |
| CFG_SA | 10 | 3.7394 | 0.7771 | 0.9033 | 0.9443 | 14.6937 |
| CFG_SA | 15 | 4.5527 | 0.7673 | 0.8923 | 0.9354 | 14.7858 |

`CFG_CA/layer_15` 的审计证据：

- `paper_level_status`: `full_evaluator_metrics_computed`
- `hook_call_counts`: `forward_with_cfg=6850`, `capture_hook=6850`, `replace_hook=6850`
- `replacement_checks`: `captured_uncond=6850`, `replaced_cond=6850`, `missed_replacement=0`, `shape_mismatch=0`
- official settings: `cfg=5.5`, `sample_steps=32`, `acc=3`, `unit_length=2`
- metrics hash: `b1aa814911f36e3f01b470b2b8c56046a45dce5c7c0aed1c7d175d2baa10a1da`

## 层趋势视图

![MoLingo FID_TMR layer trend](../visualization/figures/molingo_fid_tmr.svg)

![MoLingo Top1 layer trend](../visualization/figures/molingo_top1.svg)

![MoLingo Top2 layer trend](../visualization/figures/molingo_top2.svg)

![MoLingo Top3 layer trend](../visualization/figures/molingo_top3.svg)

## 解读

- `CFG_CA/layer_15` 是 MoLingo 中最严重的退化点：FID_TMR 从 baseline 3.5944 升到 7.7003，Top1 从 0.7755 降到 0.7240，Top3 从 0.9402 降到 0.9165。
- CA 与 CFG_SA 的 layer 15 也有 FID_TMR 升高，但检索指标保持得更好；`CFG_CA/layer_15` 同时伤害 quality proxy 和 retrieval proxy。
- MoLingo 和 MotionCLR 都在 late CFG_CA 出现明显风险。这个跨模型现象是 hard evidence；“源于通用 CFG cond/uncond 深层融合脆弱性”仍是 hypothesis，需要 cond/uncond 表征诊断、scale sweep 和 natural-representation check。
- 与 MotionCLR 的跨模型比较结论是：两个模型都出现 late CFG_CA 退化，但退化形态不同。MotionCLR 的 Top3 崩塌更极端；MoLingo 的 FID_TMR 增幅更大，但 Top3 仍保留在 0.9165。

## 与 LDO 的关系

MoLingo LDO 只有 diagnostic arrays，不是 official evaluator。特别是 late endpoint layer 15 与 baseline 距离为 0，是因为 layer 15 是最后一层，后面没有 TransformerDecoder layer 可替换为 `Identity`；这不能证明 layer 15 不重要。`CFG_CA/layer_15` official eval 直接证明该层干预会造成严重退化。

详见 [LDO/DSO 诊断报告](ldo_dso.md)。
