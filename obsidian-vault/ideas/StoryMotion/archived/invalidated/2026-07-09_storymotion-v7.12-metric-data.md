---
title: "StoryMotion v7.12 Metric Data"
status: superseded
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - metric
  - data
  - status/superseded
aliases:
  - StoryMotion-v7.12-Metric-Data
source_notes:
  - "[[2026-07-07_storymotion-v7.5-clean-data-and-human-reconstruction]]"
created: 2026-07-07T00:00:00+0800
updated: 2026-07-11T11:33:00+0800
---

# StoryMotion v7.12 Metric Data

> [!warning] Superseded ledger
> 本页混有受旧 local Stage1 契约错误影响的历史指标。当前正式证据台账已迁移至 [[2026-07-11_storymotion-v7.14-corrected-results]]。

> [!abstract] Scope
> 本页只保留 full-data 官方 metric 证据。旧 subset、feature-space MSE、training loss、stepwise checkpoint 指标已从正式 metric ledger 删除；这些内容只能作为 debug artifact，不作为公平对比表。

> [!note] Version note
> 文件名保留创建时的 v7.5 历史名；本页内容已经更新到 v7.12，以正文和 frontmatter 版本为准。

## 0. Fair Comparison Rules

| scope | exact data | samples | metric family | compare with | do not compare with |
| --- | --- | ---: | --- | --- | --- |
| full mixed official | official PulpMotion `mixed_` test | 10549 | PulpMotion official callbacks | full mixed rows | pure / paired `4053`, clean-cache rows |
| full pure official | official PulpMotion `pure_` test | 4053 | PulpMotion official callbacks | full pure rows | full mixed rows |
| original paired full Stage1 | unfiltered paired human/camera manifests; sample ids exactly match official `pure_` test | 4053 | official callbacks after decoded Stage1 reconstruction | official Pulp pure Stage1 recon and other paired tokenizer rows | clean-mixed cache, old subset rows |
| clean-mixed cache | conservative clean cache from `cache_mixed_full_clean_initial` | train 75682 / val 8399 | data-cleaning and clean fine-tune diagnostics | clean-cache controls only | tokenizer official recon rows |

Clean-mixed was used for the conservative cleaning cache, clean fine-tune, and clean-val human reconstruction diagnosis. The Stage1 tokenizer retraining/eval rows below are **not** clean-mixed; they use unfiltered original paired full data whose test ids equal official `pure_` `4053`.

## 1. Full Mixed Official Anchors

口径：official `mixed_` test `10549` samples, official callbacks, bs64 unless noted.

| model | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT human | human | 10549 | -0.00 | 17.71 | 100.0% | - | - | - | - | - | oracle reference |
| official pretrained Pulp Stage1 AE | human | 10549 | 124.46 | 18.17 | 85.4% | - | - | - | - | - | official pretrained tokenizer upper bound |
| official pretrained Pulp Stage1 AE | camera | 10549 | - | - | - | 15.51 | 58.10 | 87.2% | 0.670 | - | official pretrained tokenizer upper bound |
| official pretrained Pulp Stage1 AE | joint | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% | official pretrained tokenizer upper bound |
| self-trained Pulp Stage1 AE epoch325 | joint | 10549 | 421.87 | 9.183 | 34.7% | 41.40 | 40.18 | 72.3% | 0.406 | 22.9% | 20260708 local runner rerun; far below official pretrained |
| StoryMotion v6 unified | human | 10549 | 126.71 | 18.17 | 84.6% | - | - | - | - | - | clean human completion anchor |
| StoryMotion v6 unified | camera | 10549 | - | - | - | 14.50 | 54.85 | 87.1% | 0.638 | - | clean camera completion anchor |
| StoryMotion v6 unified | joint | 10549 | 155.73 | 23.95 | 36.4% | 85.70 | 33.52 | 62.8% | 0.374 | 7.9% | joint generation still weaker than completion |
| CondMDI RF ablation | camera | 10549 | - | - | - | 11.99 | - | - | 0.637 | - | RF keeps clean camera completion |
| CondMDI RF ablation | joint | 10549 | 206.89 | - | - | 219.36 | - | - | 0.159 | 10.4% | RF damages joint generation |

## 2. Full Pure Official Anchors

口径：official `pure_` test `4053` samples, official callbacks. The original paired full Stage1 tokenizer eval uses the same sample id set.

| model | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity | human | 4053 | -0.00 | 16.47 | 100.0% | - | - | - | - | - | oracle reference |
| GT identity | camera | 4053 | - | - | - | -0.00 | 70.24 | 100.0% | 0.945 | - | oracle reference |
| GT identity | joint | 4053 | -0.00 | 16.47 | 100.0% | -0.00 | 70.24 | 100.0% | 0.945 | 0.7% | oracle reference |
| official pretrained Pulp Stage1 AE | human | 4053 | 109.34 | 15.94 | 92.4% | - | - | - | - | - | official pretrained tokenizer upper bound |
| official pretrained Pulp Stage1 AE | camera | 4053 | - | - | - | 17.66 | 60.53 | 84.5% | 0.776 | - | official pretrained tokenizer upper bound |
| official pretrained Pulp Stage1 AE | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | official pretrained tokenizer upper bound |
| v7.14 corrected joint AE | joint | 4053 | 31.10 | 14.99 | 97.9% | 0.48 | 69.46 | 99.5% | 0.927 | 5.1% | normalized human199 + official joint camera14; step 636000 |
| v7.14 corrected joint VAE | joint | 4053 | 69.61 | 13.77 | 93.1% | 2.28 | 68.45 | 97.7% | 0.914 | 7.9% | normalized human199 + official joint camera14; step 636000 |
| self-trained Pulp Stage1 AE epoch325 | joint | 4053 | 446.11 | 8.295 | 40.9% | 55.24 | 43.99 | 73.3% | 0.500 | 18.8% | 20260708 local runner rerun; does not reproduce official pretrained |
| StoryMotion v6 unified | human | 4053 | 111.14 | 16.00 | 91.9% | - | - | - | - | - | pure human completion anchor |
| StoryMotion v6 unified | camera | 4053 | - | - | - | 23.36 | 58.41 | 83.6% | 0.763 | - | pure camera completion anchor |
| StoryMotion v6 unified | joint | 4053 | 137.12 | 21.25 | 46.4% | 91.47 | 44.46 | 61.3% | 0.594 | 6.9% | pure joint remains weaker |
| PulpMotion Stage2 no-Aux | joint | 4053 | 377.55 | 20.60 | 15.0% | 93.02 | 36.55 | 49.8% | 0.489 | 38.4% | generated joint baseline |
| PulpMotion Stage2 Aux | joint | 4053 | 419.24 | 21.69 | 14.6% | 90.62 | 38.90 | 44.8% | 0.520 | 27.1% | generated joint baseline |

## 3. Stage1 Tokenizer Official Reconstruction

Script:

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_joint_tokenizer_official_recon.py
```

Remote output directory:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260708
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260709
```

口径：unfiltered original paired full test `4053` samples, same ids as official `pure_`; each sample is reconstructed at its real valid length, then padded back to the official metric batch. This avoids non-causal convolution seeing future padding zeros.

| tokenizer experiment | data scope | setting | samples | bs | official metric status | output |
| --- | --- | --- | ---: | ---: | --- | --- |
| official pretrained Pulp Stage1 AE | full pure official | pretrained original-mixed tokenizer | 4053 | 64 | complete; see §2 | existing official upper bound |
| self-trained Pulp Stage1 AE 20260701 | original Pulp mixed train | reconstructed stage-1 script; not strict official | 4053 | 64 | non-strict; do not rank as official reproduction | prior retrain used a local runner because public PulpMotion has no AE training entrypoint |
| self-trained Pulp Stage1 AE 20260708 rerun | original Pulp mixed train | 5090 GPU3 rerun of 20260701 local runner; epoch325 | 4053 / 10549 | 64 | complete; far below pretrained upper bound | `selftrained_pulp_ae_epoch325_pure4053_bs64.json`; `selftrained_pulp_ae_epoch325_mixed10549_bs64.json` |
| joint AE human-stronger | original paired full | causal; human-stronger Stage1 objective | 4053 | 64 | complete | `joint_ae_human_stronger_pure4053_bs64.json` |
| joint VAE human-stronger | original paired full | causal; human-stronger Stage1 objective | 4053 | 64 | complete | `joint_vae_human_stronger_pure4053_bs64.json` |
| joint GRFSQ human-stronger | original paired full | causal temporal conv; GRFSQ quantizer is not a temporal module | 4053 | 64 | complete | `joint_grfsq_human_stronger_pure4053_bs64.json` |
| joint HFSQ human-stronger | original paired full | causal temporal conv; HFSQ quantizer is not a temporal module | 4053 | 64 | complete | `joint_hfsq_human_stronger_pure4053_bs64.json` |
| joint VAE original objective, non-causal | original paired full | non-causal temporal conv | 4053 | 64 | complete | `joint_vae_noncausal_original_pure4053_bs64.json` |
| joint VAE human-stronger, non-causal | original paired full | non-causal temporal conv | 4053 | 64 | complete | `joint_vae_noncausal_human_stronger_pure4053_bs64.json` |
| separate VAE original objective, non-causal | original paired full | non-causal separate branches | 4053 | 64 | complete | `separate_vae_noncausal_original_pure4053_bs64.json` |
| separate VAE human-stronger, non-causal | original paired full | non-causal separate branches | 4053 | 64 | complete | `separate_vae_noncausal_human_stronger_pure4053_bs64.json` |
| joint GRFSQ human-stronger, non-causal | original paired full | non-causal temporal conv; human-stronger objective | 4053 | 64 | complete | `joint_grfsq_noncausal_human_stronger_pure4053_bs64.json` |
| joint HFSQ human-stronger, non-causal | original paired full | non-causal temporal conv; human-stronger objective | 4053 | 64 | complete | `joint_hfsq_noncausal_human_stronger_pure4053_bs64.json` |
| separate GRFSQ human-stronger, non-causal | original paired full | non-causal separate branches; human-stronger objective | 4053 | 64 | complete | `separate_grfsq_noncausal_human_stronger_pure4053_bs64.json` |
| separate HFSQ human-stronger, non-causal | original paired full | non-causal separate branches; human-stronger objective | 4053 | 64 | complete | `separate_hfsq_noncausal_human_stronger_pure4053_bs64.json` |
| separate AE v7.12 original objective, non-causal | original paired full ae_train_split | non-causal separate branches; author default objective | 4053 | 64 | complete | `separate_ae_v7_12_correct_fast_pure4053_bs64.json` |
| separate VAE v7.12 original objective, non-causal | original paired full ae_train_split | non-causal separate branches; author default objective | 4053 | 64 | complete | `separate_vae_v7_12_correct_fast_pure4053_bs64.json` |
| separate GRFSQ v7.12 original objective, non-causal | original paired full ae_train_split | non-causal separate branches; author default objective | 4053 | 64 | complete | `separate_grfsq_v7_12_correct_fast_pure4053_bs64.json` |
| joint AE v7.13 original objective, non-causal | original paired full ae_train_split | non-causal joint branches; author default objective | 4053 | 64 | complete | `joint_ae_v7_13_default_pure4053_bs64.json` |
| joint VAE v7.13 original objective, non-causal | original paired full ae_train_split | non-causal joint branches; author default objective | 4053 | 64 | complete | `joint_vae_v7_13_default_pure4053_bs64.json` |
| joint HFSQ v7.13 original objective, non-causal | original paired full ae_train_split | non-causal joint branches; author default objective; HFSQ velocity preset `0.5` | 4053 | 64 | complete | `joint_hfsq_v7_13_default_pure4053_bs64.json` |

Completed official joint metrics:

| tokenizer experiment | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT identity | 4053 | -0.00 | 16.47 | 100.0% | -0.00 | 70.24 | 100.0% | 0.945 | 0.7% |
| official pretrained Pulp Stage1 AE | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| self-trained Pulp Stage1 AE epoch325 | 4053 | 446.11 | 8.295 | 40.9% | 55.24 | 43.99 | 73.3% | 0.500 | 18.8% |
| joint AE human-stronger | 4053 | 1478.33 | 0.000 | 0.2% | 594.70 | 10.71 | 1.2% | 0.513 | 33.2% |
| joint VAE human-stronger | 4053 | 1513.27 | 0.000 | 0.1% | 737.71 | 7.90 | 0.8% | 0.494 | 29.5% |
| joint GRFSQ human-stronger | 4053 | 1586.13 | 2.320 | 0.1% | 679.49 | 10.75 | 1.2% | 0.343 | 27.3% |
| joint HFSQ human-stronger | 4053 | 1493.25 | 3.252 | 0.0% | 392.53 | 20.57 | 8.4% | 0.330 | 20.5% |
| joint VAE original objective, non-causal | 4053 | 1250.40 | 8.443 | 0.7% | 110.66 | 45.89 | 65.7% | 0.533 | 20.4% |
| joint VAE human-stronger, non-causal | 4053 | 1281.96 | 8.685 | 0.9% | 149.72 | 40.55 | 55.9% | 0.497 | 20.2% |
| separate VAE original objective, non-causal | 4053 | 1183.18 | 7.351 | 1.0% | 23.42 | 59.80 | 87.5% | 0.795 | 20.7% |
| separate VAE human-stronger, non-causal | 4053 | 1211.04 | 8.414 | 0.9% | 27.46 | 58.69 | 87.2% | 0.795 | 20.7% |
| joint GRFSQ human-stronger, non-causal | 4053 | 1301.26 | 8.743 | 0.6% | 159.97 | 29.80 | 45.4% | 0.343 | 20.5% |
| joint HFSQ human-stronger, non-causal | 4053 | 1385.16 | 7.051 | 0.1% | 116.82 | 30.73 | 44.0% | 0.327 | 11.8% |
| separate GRFSQ human-stronger, non-causal | 4053 | 1269.24 | 7.054 | 0.7% | 188.71 | 32.90 | 45.9% | 0.391 | 19.7% |
| separate HFSQ human-stronger, non-causal | 4053 | 1366.50 | 7.778 | 0.2% | 83.04 | 41.54 | 62.9% | 0.448 | 19.3% |
| separate AE v7.12 original objective, non-causal | 4053 | 1239.97 | 8.044 | 1.0% | 22.90 | 61.03 | 83.4% | 0.930 | 20.8% |
| separate VAE v7.12 original objective, non-causal | 4053 | 1219.41 | 9.223 | 1.1% | 15.14 | 63.57 | 89.8% | 0.928 | 20.8% |
| separate GRFSQ v7.12 original objective, non-causal | 4053 | 1281.73 | 9.111 | 0.7% | 59.37 | 48.54 | 69.3% | 0.610 | 20.7% |
| joint AE v7.13 original objective, non-causal | 4053 | 1190.17 | 8.096 | 0.9% | 33.57 | 58.55 | 80.3% | 0.852 | 20.8% |
| joint VAE v7.13 original objective, non-causal | 4053 | 1232.87 | 8.736 | 0.8% | 44.00 | 54.64 | 75.7% | 0.775 | 20.5% |
| joint HFSQ v7.13 original objective, non-causal | 4053 | 1467.24 | 10.852 | 0.3% | 116.20 | 36.19 | 51.4% | 0.447 | 20.8% |

No loss or feature-space MSE is reported in this ledger.

## 4. v7.12 Metric Divergence Diagnosis

v7.12 的核心现象不是“整体变好”或“整体变坏”，而是 metric family 明显分裂：camera-side 与 caption F1 大幅改善，但 human TMR-family 和 joint projection 没有恢复。

| row | compare target | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT identity | no-generation oracle | -0.00 | 16.47 | 100.0% | -0.00 | 70.24 | 100.0% | 0.945 | 0.7% |
| official pretrained Pulp AE | pure official upper bound | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| self-trained Pulp AE epoch325 | old local self-retrain | 446.11 | 8.295 | 40.9% | 55.24 | 43.99 | 73.3% | 0.500 | 18.8% |
| v7.12 separate AE default | new separate default | 1239.97 | 8.044 | 1.0% | 22.90 | 61.03 | 83.4% | 0.930 | 20.8% |
| v7.12 separate VAE default | new separate default | 1219.41 | 9.223 | 1.1% | 15.14 | 63.57 | 89.8% | 0.928 | 20.8% |
| v7.12 separate GRFSQ default | new separate default | 1281.73 | 9.111 | 0.7% | 59.37 | 48.54 | 69.3% | 0.610 | 20.7% |
| v7.13 joint AE default | new joint default | 1190.17 | 8.096 | 0.9% | 33.57 | 58.55 | 80.3% | 0.852 | 20.8% |
| v7.13 joint VAE default | new joint default | 1232.87 | 8.736 | 0.8% | 44.00 | 54.64 | 75.7% | 0.775 | 20.5% |
| v7.13 joint HFSQ default | new joint default | 1467.24 | 10.852 | 0.3% | 116.20 | 36.19 | 51.4% | 0.447 | 20.8% |

直接读数：

- 相对旧 self-retrain，v7.12/v7.13 的 FDTMR 从 `446.11` 恶化到 `1190-1467`，HCov 从 `40.9%` 掉到约 `0.3-1.1%`；这是 human embedding distribution collapse，不是普通 loss 差异。
- 相对 official pretrained pure anchor，v7.12/v7.13 的 TMR 多数只有 `8-11`，明显低于 `15.94`；Out 约 `20.5-20.8%`，也远高于 official `3.5%`。
- v7.12 separate VAE 的 camera-side 指标最强：FDCLaTr `15.14`、CLaTr `63.57`、CCov `89.8%`、F1 `0.928`。v7.13 joint AE 次之，FDCLaTr `33.57`、F1 `0.852`，但仍没有恢复 human TMR-family 或 Out。

最可能原因：

- `F1` 是 camera caption / camera motion segment 侧指标，不是 human motion semantic 指标。它可以因为 camera trajectory 更规则、更可分而提升，即使 human TMR embedding 已经偏离真实 motion manifold。
- separate branch 训练削弱了 human-camera 的联合约束。camera branch 单独重建得更好时，FDCLaTr / CLaTr / F1 会改善；但 joint projection 的 Out 仍依赖 human motion、camera trajectory、可见性和同步关系，单分支优秀不能保证 Out 下降。
- HCov 接近 `1%` 表示 decoded human embeddings 只覆盖极窄区域或落在 TMR real manifold 外。它比单帧视觉观感更敏感，可能由 root/global normalization、RIFKE-to-joint 解码动态、decoder 末端边界、速度统计过平滑或 TMR 预处理契约不匹配触发。
- v7.12 使用 `ae_train_split` 上的 local retrain / last checkpoint，而 official pretrained 是 PulpMotion 官方 tokenizer 上界。两者训练数据、checkpoint 选择和实现入口不同；official pretrained 条目必须保留为 upper bound，不能用 local self-retrain 代替。
- §10 的 last-frame / decoder-boundary 诊断会放大 TMR 与 Out：局部末端形变对 caption F1 影响小，但会扰动 human motion embedding 和投影可见性。

下一步诊断应优先做分支置换，而不是继续看 loss：`GT human + v7.12 camera`、`v7.12 human + GT camera`、`official pretrained human + v7.12 camera` 三组能直接区分 Out 恶化来自 human、camera，还是配对同步。另一个必要检查是导出 TMR encoder 输入前的 motion 统计，比较 official pretrained、self-retrain、v7.12 的 root、velocity、valid length 与最后几帧误差。

## 5. Full Mixed Stage2 Rows Kept For Context

Only full-data official rows are retained here. Old subset rows and stepwise checkpoint sweeps are intentionally absent.

| group | task | samples | core result | decision |
| --- | --- | ---: | --- | --- |
| full tokenizer Stage2, separate VAE with-z | joint | 10549 | FDTMR `1863.90`, TMR `0.000`, FDCLaTr `885.36`, F1 `0.057`, Out `99.0%` | negative |
| full tokenizer Stage2, joint VAE / GRFSQ | joint | 10549 | full train/eval did not close the gap to StoryMotion v6 or official Pulp upper bound | negative |
| v7.3.1 one-hot reliability | three-mode | 10549 | joint improved relative to several local ablations but remained below clean unified baseline | candidate evidence only |
| v7.4 minimal human-input shuffle | three-mode | 10549 | camera completion improved but joint FDTMR / FDCLaTr / F1 regressed vs one-hot reliability | rejected repair |
| MoLingo FullRF p2b H2C | H2C | 10549 | clean FDCLaTr `22.67`, F1 `0.590`; noisy `0.15` FDCLaTr `40.41`, F1 `0.452` | H2C robustness candidate, not unified final |

## 6. Removed From Formal Metric Ledger

- Removed all subset rows because they are not full-data experiments.
- Removed training loss and feature-space MSE tables because the user-requested eval is official metric eval, not loss comparison.
- Removed stepwise checkpoint metric sweeps from this page. If needed, they should live in raw run artifacts or a debug note, not in the formal comparison ledger.
- Removed invented version-style labels from experiment naming. Existing remote directory names are treated as artifact paths, not experiment names.
