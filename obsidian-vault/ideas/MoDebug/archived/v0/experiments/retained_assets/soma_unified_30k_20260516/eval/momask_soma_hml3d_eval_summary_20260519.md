---
title: "MoMask SOMA 30k 评估汇总"
created: 2026-05-19T15:25:31+08:00
updated: 2026-05-19T15:25:31+08:00
type: eval_summary
tags:
  - MoDebug
  - SOMA
  - MoMask
  - eval
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]"
---
# MoMask SOMA 30k 评估汇总

## 目标

记录 4090 上 SOMA 子集训练的 MoMask 在两个 test set 上的官方 generation eval，并给出两个对照：

- SOMA 子集 test 指标 vs Kimodo full dataset 训练的论文侧参考指标。
- SOMA 子集训练、HumanML3D test 指标 vs MoMask 原论文 HumanML3D 指标。

## 协议

- 远端代码: `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518`
- 模型:
  - VQ: `soma30k_full29998_rvq6_bs512_noanim_20260518`
  - masked transformer: `soma30k_full29998_mtrans_bs64_noanim_20260518`
  - residual transformer: `soma30k_full29998_rtrans_bs64_noanim_20260518`
- 评估脚本: `eval_t2m_trans_res.py`
- 命令参数: `--which_epoch latest --cond_scale 4 --time_steps 10 --temperature 1 --topkr 0.9`
- repeat 数: `20`
- 置信区间: 官方脚本报告 `1.96 * std / sqrt(20)`
- checkpoint 行为:
  - masked transformer 加载 `latest.tar`，日志显示 epoch `499`
  - residual transformer 由脚本硬编码加载 `net_best_fid.tar`，日志显示 epoch `2`
- 数据集切换:
  - 先把 `dataset/HumanML3D` 指向 SOMA converted HumanML3D-263 root
  - 再指向 official HumanML3D root
  - 退出时 cleanup 已恢复原始 SOMA dataset symlink

产物:

- SOMA final log: [[artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/soma_test_latest_cs4_ts10_rep20_20260519.log]]
- HumanML3D final log: [[artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/hml3d_test_latest_cs4_ts10_rep20_20260519.log]]
- 完整远端运行日志: [[artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/soma30k_momask_eval_soma_hml3d_gpu1_20260519.log]]
- artifact hashes: [[artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/sha256.txt]]

## MoMask 评估结果

| 训练数据                         |                    测试数据 | n/evaluable |          FID↓ |     Diversity |         Top1↑ |         Top2↑ |         Top3↑ |     Matching↓ | Multimodality↑ |
| ---------------------------- | ----------------------: | ----------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | -------------: |
| SOMA converted HumanML3D-263 |               SOMA test |   3000/3000 | 3.324 ± 0.013 | 7.846 ± 0.069 | 0.189 ± 0.002 | 0.320 ± 0.002 | 0.416 ± 0.003 | 4.897 ± 0.006 |  1.151 ± 0.044 |
| SOMA converted HumanML3D-263 | HumanML3D official test |   4384/4384 | 6.330 ± 0.040 | 7.330 ± 0.076 | 0.208 ± 0.002 | 0.342 ± 0.002 | 0.441 ± 0.002 | 5.464 ± 0.009 |  1.605 ± 0.052 |

## HumanML3D vs MoMask 原论文

MoMask 参考来源：[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]] paper Table 1, HumanML3D test set。

| 来源 | 训练数据 | 测试数据 | Top1↑ | Top2↑ | Top3↑ | FID↓ | Matching / MM-Dist↓ | Multimodality↑ |
|---|---|---|---:|---:|---:|---:|---:|---:|
| SOMA 30k MoMask run | SOMA converted HumanML3D-263 | HumanML3D official test | 0.208 | 0.342 | 0.441 | 6.330 | 5.464 | 1.605 |
| MoMask paper | HumanML3D | HumanML3D test | 0.521 | 0.713 | 0.807 | 0.045 | 2.958 | 1.241 |

相对 MoMask 原论文 HumanML3D 结果，SOMA-trained checkpoint 在同一大类 benchmark 口径下明显更差：FID 是 `6.330` vs `0.045`，Top3 是 `0.441` vs `0.807`，matching distance 是 `5.464` vs `2.958`。这只能支持跨数据 sanity 结论：该 SOMA-trained model 在 official HumanML3D evaluator 下没有迁移到 HumanML3D-level text-motion alignment。

## 结论

- SOMA test：本次 MoMask run 可以端到端评估，但 HumanML3D evaluator 在这个 converted SOMA 分布上给出的语义检索对齐较弱。
- HumanML3D test：同一个 checkpoint 显著低于 MoMask paper HumanML3D 结果，因此不能当作 general HumanML3D model。
- Kimodo 对照：只保留为 paper-side reference；除非构建共同 evaluator 和共同 test distribution，否则不能作为 formal ordering evidence。
- 本次 official eval 使用的 residual checkpoint 是 epoch `2` 的 `net_best_fid.tar`；这是脚本行为，需要保留在 provenance 里。

## 元数据

- date: `2026-05-19`
- artifact_path: `artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/`
- evaluator: `MoMask eval_t2m_trans_res.py + HumanML3D Comp_v6_KLD005 evaluator; Kimodo paper Table 2; MoMask paper Table 1`
- protocol: `20-repeat official generation eval; cond_scale=4, time_steps=10, temperature=1, topkr=0.9; masked latest.tar; residual net_best_fid.tar`
- motion_source: `SOMA converted HumanML3D-263 test root and official HumanML3D test root`
- data_source: `soma30k_momask_eval_soma_hml3d_gpu1_20260519.log; soma_test_latest_cs4_ts10_rep20_20260519.log; hml3d_test_latest_cs4_ts10_rep20_20260519.log; MoMask CVPR 2024 Table 1; Kimodo arXiv 2026 Table 2`
- condition_pair: `SOMA-trained MoMask -> SOMA test; SOMA-trained MoMask -> HumanML3D test`
- n/evaluable: `3000/3000 SOMA test; 4384/4384 HumanML3D test`
- coverage: `仅 official text-to-motion generation metrics；不含 human preference、visual audit 或 common Kimodo evaluator`
- role: `cross_check`
- used_for: `observation`
- limitations: `KIMODO metrics 与 MoMask HumanML3D evaluator metrics 不可直接比较；HumanML3D 对照只是 paper numbers sanity check，不是 held-out final evaluation；residual checkpoint 是 best-FID epoch 2，不是 residual latest；本 summary 未做人眼可视化检查。`
