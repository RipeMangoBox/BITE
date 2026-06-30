---
title: "StoryMotion v6.2 Metric Data"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - metric
  - data
  - status/active
aliases:
  - StoryMotion-v6.2-Metric-Data
source_notes:
  - "[[2026-06-29_storymotion-v6.2]]"
  - "[[2026-06-30_storymotion-experiment-metric-comparison]]"
created: 2026-07-01T02:47:56+0800
updated: 2026-07-01T02:47:56+0800
---

## Full Mixed Official Eval 2026-07-01

口径：5090 上使用 `scripts/storymotion_official_full_eval.py`，`batch_size=64`、`seed=17`、`num_steps=50`、`cfg_scale=1.0`、`eta=0.0`，full mixed test `10549` samples。4090 GPU1 的 joint GRFSQ full Stage1/后续实验仍在队列中，本节不纳入。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MoLingo human-only | full-train | mixed | human | 10549 | 2396.07 | 4.112 | 0.04% | - | - | - | - | - | 12.1% | 0.344 | negative; full train does not rescue human baseline |
| separate AE no-z | full-train | mixed | human | 10549 | 2147.78 | 5.547 | 0.03% | - | - | - | - | - | 6.0% | 0.385 | negative |
| separate AE no-z | full-train | mixed | camera | 10549 | - | - | - | 676.56 | 2.794 | 1.00% | 0.084 | - | 6.2% | 0.384 | negative |
| separate AE no-z | full-train | mixed | joint | 10549 | 2157.12 | 5.669 | 0.00% | 662.84 | 3.074 | 1.11% | 0.094 | 95.5% | 6.9% | 0.387 | negative; joint generation collapses |
| separate VAE with-z | full-train | mixed | human | 10549 | 1823.40 | 0.000 | 0.05% | - | - | - | - | - | 8.2% | 0.294 | negative; TMR score collapsed |
| separate VAE with-z | full-train | mixed | camera | 10549 | - | - | - | 841.65 | 3.884 | 0.69% | 0.099 | - | 7.5% | 0.295 | negative |
| separate VAE with-z | full-train | mixed | joint | 10549 | 1863.90 | 0.000 | 0.00% | 885.36 | 3.785 | 0.39% | 0.057 | 99.0% | 7.9% | 0.297 | negative; worse than mixed-subset trend |

## Mixed-Subset To Full Readout

这张表只比较同一实验族的趋势，不把 subset 与 full 当作公平排名。结论是：旧 mixed-subset 结果不是“eval 少跑 formal test”造成的偶然缺口；补 full train/full eval 后，MoLingo、separate AE no-z、separate VAE with-z 仍不能 promoted。

| experiment | old mixed-subset row | full mixed row | readout |
| --- | --- | --- | --- |
| MoLingo human-only human | `3279` samples, FDTMR `2353.96`, TMR `4.466`, HCov `0.1%` | `10549` samples, FDTMR `2396.07`, TMR `4.112`, HCov `0.04%` | full train does not improve baseline quality |
| separate AE no-z human | `3279` samples, FDTMR `2018.28`, TMR `4.450`, HCov `0.1%` | `10549` samples, FDTMR `2147.78`, TMR `5.547`, HCov `0.03%` | still negative |
| separate AE no-z camera | `3279` samples, FDCLaTr `623.87`, CLaTr `8.476`, F1 `0.074` | `10549` samples, FDCLaTr `676.56`, CLaTr `2.794`, F1 `0.084` | still far from valid camera rows |
| separate AE no-z joint | `3279` samples, FDTMR `2031.69`, FDCLaTr `583.11`, Out `93.7%` | `10549` samples, FDTMR `2157.12`, FDCLaTr `662.84`, Out `95.5%` | joint remains collapsed |
| separate VAE with-z human | `3279` samples, FDTMR `1274.72`, TMR `7.076`, HCov `0.6%` | `10549` samples, FDTMR `1823.40`, TMR `0.000`, HCov `0.05%` | full mixed is worse |
| separate VAE with-z camera | `3279` samples, FDCLaTr `118.77`, CLaTr `38.08`, F1 `0.472` | `10549` samples, FDCLaTr `841.65`, CLaTr `3.884`, F1 `0.099` | subset optimism does not transfer |
| separate VAE with-z joint | `3279` samples, FDTMR `1316.47`, FDCLaTr `133.95`, Out `39.4%` | `10549` samples, FDTMR `1863.90`, FDCLaTr `885.36`, Out `99.0%` | full joint fails decisively |

## Evidence

- metric eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`
- eval logs: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701/logs`
- full-train logs: `/data/public/ripemangobox/Motion/StoryMotion/logs/v6_2_fulltrain_20260630`
- MoLingo full run: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_molingo_human_seed17_fulltrain_20260630/human_only_b512_full`
- separate AE no-z full run: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_separate_ae_noz_seed17_fulltrain_20260630/mixed_b512_full`
- separate VAE with-z full run: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_separate_vae_wz_seed17_fulltrain_20260630/mixed_b512_full`
- full camera manifests: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_*_manifest_full_20260630.jsonl`
