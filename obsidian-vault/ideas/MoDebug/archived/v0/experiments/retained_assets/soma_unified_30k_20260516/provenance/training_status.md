---
title: "SOMA Unified 30k 训练状态"
created: 2026-05-16T23:48:36
updated: 2026-05-19T15:25:31+08:00
type: training_status
---

# SOMA Unified 30k 训练状态

## 目标

记录 MoMask/MoGenTS 基于 full text + full motion sequence retrain 的当前状态、blocker 和下一步，不宣称未完成的训练效果。

## 数据对象

- dataset manifest hash: `e07963cde7e86b2db43a264237ef533954e6e703f659a82eda88d5e7393c57ac`
- split manifest hash: `e07963cde7e86b2db43a264237ef533954e6e703f659a82eda88d5e7393c57ac`
- remote raw text-motion manifest: `remote4090_build/manifests/selected_30k_text_motion_manifest.tsv`
- remote dataset root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/text_motion_dataset`
- HumanML3D smoke dataset root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_smoke_20260517/hml3d_dataset`
- HumanML3D 20fps smoke dataset root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_smoke_20fps_20260517/hml3d_dataset`
- HumanML3D 30k 20fps conversion root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_30k_20fps_20260517`
- HumanML3D clean_min40 training root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_30k_20fps_clean_min40_20260518`
- local pulled artifacts: `artifacts/remote4090/remote4090_soma30k_clean_train_20260518/soma30k_clean_train_20260518/`
- MoMask eval artifacts: `artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/`
- MoMask remote code root: `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518`
- training jobs: MoMask、MoGenTS。

## 4090 Raw Text-Motion 构造状态

| item | status |
|---|---|
| uploaded manifest/split hash check | ok |
| motion symlinks | 30000/30000 |
| text files | 30000/30000 |
| missing motion | 0 |
| split counts | train=24000, val=3000, test=3000 |
| source_identity leakage overlap | none |
| local pullback location | `remote4090_build/` |

## KIMODO/HumanML3D 转换 Smoke 状态

| item | status |
|---|---|
| KIMODO official BVH -> NPZ | 6/6 ok |
| HumanML3D 263D `new_joint_vecs` | 6/6 ok |
| recovered 22-joint visualization | 6 PNG panels |
| local feature shape check | all `[T, 263]`, finite |
| loader smoke | pass |
| local pullback location | `humanml3d_smoke_20260517/` |

## KIMODO/HumanML3D 20fps Gate 状态

| item | status |
|---|---|
| KIMODO axis convention | 文档和输出链路按 Y-up、+Z forward；HumanML3D/MoGenTS 也以 Y 为高度、XZ 为地面平面。 |
| 20fps conversion smoke | `6/6` ok，loader smoke pass，本地拉回 `humanml3d_smoke_20fps_20260517/`。 |
| 20fps regression | `12/12` ok，loader smoke pass，`vis_limit=3`、`hash_mode=summary`。 |
| full 30k conversion | completed at 2026-05-17T23:54:53+08:00，log `logs/remote4090/soma30k_hml3d_full20fps_20260517.log`。 |
| converted rows | `29998/30000`; failed rows: `soma30k_11404`, `soma30k_21676`，原因均为 `Non-finite feature or recovered joint value`。 |
| original loader smoke | fail；7 条 train 样本 shape 为 `(39, 263)`，低于 `min_motion_len=40`。 |
| clean_min40 view | train=23991, val=3000, test=3000, all=29991；Mean/Std 在 clean train split 上重算。 |
| clean Mean/Std hash | mean=`cd14c5fb810d423ea10c0dcddc467d75cae4f4113e10d55c9f793bc311fe540c`; std=`1ccafc99c8372576c6cc0a5bc045d8cfcead9f14f9c75ca0c7a8c78530db7628`。 |
| MoGenTS eval loader smoke | pass；`eval_loader_len=3000`, `batch_len=8`。 |
| MoGenTS VQ dataset link | `/data/public/ripemangobox/Motion/mogents/dataset/HumanML3D -> humanml3d_30k_20fps_clean_min40_20260518`；split/file count 为 `29991`。 |
| VQ MotionDataset effective motions | `window_size=64` 下 train 保留 `20480` motions、`1070239` snippets；val 保留 `2581` motions、`136457` snippets。 |
| MoMask copied version | local `linkedCodebases/momask-codes` -> remote `momask-codes-mocritique-mvp-27687f4-20260518`; source HEAD `27687f4`, branch `mocritique-mvp`。 |
| MoMask data entry | `dataset/HumanML3D -> humanml3d_30k_20fps_20260517/hml3d_dataset`; split/file count 为 `29998`。 |

## 当前状态

| model | status | tmux_session | log_path | checkpoint_path | next_action |
|---|---|---|---|---|---|
| MoMask VQ | COMPLETED_VERIFIED | ended | `logs/remote4090/soma30k_momask_vq_gpu1_bs512_noanim_20260518.log` | `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518/checkpoints/t2m/soma30k_full29998_rvq6_bs512_noanim_20260518/model` | VQ 已完成；checkpoint preflight 通过；已启动 masked/residual transformers。 |
| MoMask masked transformer | COMPLETED_EVAL_DONE | ended | `logs/remote4090/soma30k_momask_mtrans_gpu1_20260518.log` | `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518/checkpoints/t2m/soma30k_full29998_mtrans_bs64_noanim_20260518/model` | 训练完成到 Ep500；官方 eval 使用 `latest.tar`。 |
| MoMask residual transformer | COMPLETED_EVAL_DONE | ended | `logs/remote4090/soma30k_momask_rtrans_gpu1_20260518.log` | `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518/checkpoints/t2m/soma30k_full29998_rtrans_bs64_noanim_20260518/model` | 训练完成到 Ep500；官方 eval 脚本加载 `net_best_fid.tar`，日志显示 epoch 2。 |
| MoGenTS VQ | RUNNING | `soma30k_mogents_vq_gpu0_20260518` | `logs/remote4090/soma30k_mogents_vq_gpu0_20260518.log` | `/data/public/ripemangobox/Motion/mogents/logs/humanml3d/soma30k_clean_min40_rvq6_bs128_20260518/model` | 约 `48%`；Ep 24 validation 已完成；日志剩余约 `1289 min`，按当前速度预计 2026-05-19 18:00 +08 左右结束。 |
| MoGenTS transformer | WAITING_FOR_VQ | N/A | N/A | N/A | 等待 `soma30k_clean_min40_rvq6_bs128_20260518` VQ checkpoint。 |

## 计算方式

remote4090 preflight 检查远程 repo、数据资产和训练 gate；随后按本地 manifest/split 在 4090 构造 raw BVH text-motion dataset，并转换为 HumanML3D-263。原始 full conversion 保留不改；训练使用 clean_min40 视图过滤 7 条 too-short train samples，并重算 Mean/Std。

MoGenTS VQ 启动命令：

```bash
CUDA_VISIBLE_DEVICES=0 conda run --no-capture-output -n mogents-gpu1 \
  bash run_rvq.sh soma30k_clean_min40_rvq6_bs128_20260518 0 humanml3d \
    --batch_size 128 --num_quantizers 6 --max_epoch 50 \
    --quantize_dropout_prob 0.2 --gamma 0.1 --code_dim2d 1024 --nb_code2d 256
```

MoMask VQ 启动命令：

```bash
CUDA_VISIBLE_DEVICES=1 conda run --no-capture-output -n mogents-gpu1 \
  python train_vq.py --name soma30k_full29998_rvq6_bs512_noanim_20260518 \
    --gpu_id 0 --dataset_name t2m --batch_size 512 --num_quantizers 6 \
    --max_epoch 50 --eval_every_e 999 --quantize_dropout_prob 0.2 --gamma 0.1
```

MoMask masked transformer 启动命令：

```bash
CUDA_VISIBLE_DEVICES=1 /home/ripemangobox/miniconda3/bin/conda run --no-capture-output -n mogents-gpu1 \
  python train_t2m_transformer.py \
    --name soma30k_full29998_mtrans_bs64_noanim_20260518 \
    --gpu_id 0 --dataset_name t2m --batch_size 64 \
    --vq_name soma30k_full29998_rvq6_bs512_noanim_20260518 \
    --eval_every_e 999
```

MoMask residual transformer 启动命令：

```bash
CUDA_VISIBLE_DEVICES=1 /home/ripemangobox/miniconda3/bin/conda run --no-capture-output -n mogents-gpu1 \
  python train_res_transformer.py \
    --name soma30k_full29998_rtrans_bs64_noanim_20260518 \
    --gpu_id 0 --dataset_name t2m --batch_size 64 \
    --vq_name soma30k_full29998_rvq6_bs512_noanim_20260518 \
    --cond_drop_prob 0.2 --share_weight --eval_every_e 999
```

## 结论

当前没有 held-out final evaluator 结论。4090 raw BVH text-motion 数据集已构造完成，30k full conversion 已结束但原始目录 loader smoke 失败；clean_min40 视图通过 MoGenTS eval loader smoke；MoMask VQ、masked transformer、residual transformer 均已完成，并已在 SOMA test 与 official HumanML3D test 上完成 20-repeat 官方 eval。训练仍有以下限制：

- MoMask VQ 已完成，`net_best_fid.tar`、`net_best_mm.tar`、`latest.tar` 均存在；MoMask transformer official eval 结果记录在 `eval/momask_soma_hml3d_eval_summary_20260519.md`，角色为 `cross_check`。
- 原始 full conversion 有 2 条转换失败和 7 条 too-short train samples；训练使用过滤后的 clean_min40 视图。
- MoGenTS 当前不是使用 `29998` 条 split，而是使用 clean_min40 的 `29991` 条 split；且 VQ 训练实际按 `window_size=64` 保留 `20480` 条 train motions。
- smoke 的 SOMA77->HumanML3D22 是基于拓扑/名称的映射，仍需人工检查可视化和更多样本。
- MoGenTS VQ 只是 running，不是完成；Ep 0 evaluation 和 iter loss 只作为诊断。
- MoGenTS transformer 仍需等待 VQ checkpoint。

## 2026-05-18 下午检查

- MoGenTS VQ 正常运行：GPU0 约 `9841 MiB`、`100%`，进度约 `ep/it:16-7523`, `niter:141300`, `completed:33%`。
- 近期 loss 在 `0.05-0.07` 区间波动，`loss_rec` 约 `0.011-0.023`，perplexity 约 `160-179`，未见 traceback/OOM/NaN。
- best FID checkpoint 已产出到 `model/`，包含 `net_best_fid_ep0016.tar`；`animation/` 和 `animation_eval/` 已有 E0016 mp4。
- 本地抽查 mp4：`animation_E0016_07.mp4` 为 `1000x1000`, `64` frames, `3.2s`；`animation_eval_E0016_05.mp4` 为 `1000x1000`, `196` frames, `9.8s`；抽帧 PNG 非空。
- MoMask sync 完成：远端目录 `/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518`，保留 lightweight code/glove，排除 checkpoints/generation/editing；`dataset/HumanML3D` 指向 full-conversion 29998 数据根。
- MoMask VQ loader gate 通过 import 和 `MotionDataset` 初始化；在 `window_size=64` 下 train 同样保留 `20480` motions、`1070239` snippets。
- MoMask VQ 首次启动因 `CUDA_VISIBLE_DEVICES=1` 下仍传 `--gpu_id 1` 触发 `invalid device ordinal`；已用 `CUDA_VISIBLE_DEVICES=1` + `--gpu_id 0` 修正。
- MoMask VQ `bs128` 试跑已按用户要求停止：tmux `soma30k_momask_vq_gpu1_retry_20260518`，日志保留 `logs/remote4090/soma30k_momask_vq_gpu1_retry_20260518.log`。
- MoMask VQ official batch-size 首次重跑 `soma30k_momask_vq_gpu1_bs512_20260518` 在 Ep 1 训练和验证后崩溃；根因是 `MovieWriter ffmpeg unavailable`，Matplotlib fallback 到 `PillowWriter` 后不能保存 `.mp4`，报 `ValueError: unknown file extension: .mp4`。这不是 OOM，也不是训练 loss 异常。
- MoMask VQ 已用 official batch-size 重新启动 no-animation 版本：tmux `soma30k_momask_vq_gpu1_bs512_noanim_20260518`，日志 `logs/remote4090/soma30k_momask_vq_gpu1_bs512_noanim_20260518.log`，命令加 `--eval_every_e 999` 以避免训练中保存 mp4；GPU1 约 `3125 MiB`、`100%`，已跑到 Ep 2 validation，约 `niter:4180`，日志 ETA 约 `110 min`。
- 当前 MoMask 训练环境是 `mogents-gpu1`，Python `3.8.20`、torch `2.2.0+cu118`、CUDA `11.8`，不是 Python 3.7。4090 上存在 `MoCritique` conda 环境，但该环境当前 `import torch` 失败，不能直接运行 MoMask；若切换需要先补 PyTorch/CUDA 和 MoMask 依赖。
- MoMask VQ 已完成到 Ep 50；末次 validation loss 为 `0.15982`，reconstruction `0.04031`，velocity `0.01427`，commit `5.61863`。Ep 50 diagnostic eval 为 FID `3.0942`、Diversity `8.6783`、R_precision pred `(0.1875, 0.3212, 0.4160)`、matching score pred `4.9927`。
- MoMask VQ checkpoint preflight 通过：`mean.npy` / `std.npy` shape 为 `(263,)` 且 finite；`net_best_fid.tar` 的 `ckpt_ep=36`，state tensors `72`、params `21009671`、finite；按 `RVQVAE` 加载 missing/unexpected 均为 `0`。
- MoMask masked transformer 已启动：tmux `soma30k_momask_mtrans_gpu1_20260518`，日志 `logs/remote4090/soma30k_momask_mtrans_gpu1_20260518.log`。启动后已完成 Ep 10 validation；Ep 10 diagnostic validation loss `2.952`、accuracy `0.327`、FID `5.0728`，未见 traceback/OOM/NaN。
- MoMask residual transformer 已启动：tmux `soma30k_momask_rtrans_gpu1_20260518`，日志 `logs/remote4090/soma30k_momask_rtrans_gpu1_20260518.log`。启动后已完成 Ep 4 validation；Ep 4 diagnostic validation loss `5.497`、accuracy `0.017`、FID `3.9656`，未见 traceback/OOM/NaN。
- MoGenTS VQ 仍在 GPU0 运行：约 `ep/it:24-475`、`niter:201140`、`completed:48%`，Ep 24 validation loss `0.04920`，日志剩余约 `1289 min`，按当前速度预计 2026-05-19 18:00 +08 左右结束；近期 loss 约 `0.046-0.061`，未见 traceback/OOM/NaN。

> [!warning] 指标边界
> `soma30k_mogents_vq_gpu0_20260518.log` 中的 Ep 0 FID/Top-k 和 early iter loss 是启动期诊断，不是正式模型评估，也不用于 paper ordering。

## 2026-05-19 MoMask 官方 Eval

- MoMask masked/residual transformer 训练均已跑到 Ep500，tmux session 已结束，GPU1 空闲。
- eval session: `soma30k_momask_eval_soma_hml3d_gpu1_20260519`
- full run log: `logs/remote4090/soma30k_momask_eval_soma_hml3d_gpu1_20260519.log`
- local pulled artifacts: `artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/`
- summary: `eval/momask_soma_hml3d_eval_summary_20260519.md`
- protocol: official `eval_t2m_trans_res.py`, `20` repeats, `cond_scale=4`, `time_steps=10`, `temperature=1`, `topkr=0.9`。
- checkpoint behavior: masked transformer 使用 `latest.tar`，日志显示 epoch `499`；residual transformer 按脚本加载 `net_best_fid.tar`，日志显示 epoch `2`。
- SOMA test result: FID `3.324±0.013`, Top1/2/3 `0.189/0.320/0.416`, Matching `4.897±0.006`, Multimodality `1.151±0.044`。
- HumanML3D test result: FID `6.330±0.040`, Top1/2/3 `0.208/0.342/0.441`, Matching `5.464±0.009`, Multimodality `1.605±0.052`。
- 结论边界：SOMA vs KIMODO 只能作为 paper-side reference，因为 KIMODO 使用 Rigplay/TMR evaluator；SOMA-trained MoMask 在 HumanML3D test 上显著低于 MoMask paper HumanML3D 数值，只能作为跨数据 sanity check。

## 下一步 Gate

1. 继续监控 `soma30k_mogents_vq_gpu0_20260518`，预计 2026-05-19 18:00 +08 左右结束；完成后做 checkpoint preflight，再启动 MoGenTS transformer。
2. 对 MoMask SOMA eval 做少量可视化抽检，尤其是低 Top-k / 高 Matching 的 case，判断是文本分布、骨架映射还是生成质量问题。
3. 对 clean_min40 视图做更多可视化抽检，尤其是 SOMA77->HumanML3D22 映射和 2 条 non-finite 失败样本。

## 元数据

- date: `2026-05-18`
- experiment_path: `paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`
- artifact_path: `artifacts/remote4090/remote4090_soma30k_clean_train_20260518/soma30k_clean_train_20260518/`; `artifacts/remote4090/remote4090_soma30k_mogents_momask_check_20260518/`; `artifacts/remote4090/remote4090_soma30k_mogents_vis_check_20260518/`; `artifacts/remote4090/remote4090_momask_soma_hml3d_eval_20260519/momask_soma_hml3d_eval_20260519/`; remote logs `logs/remote4090/soma30k_momask_vq_gpu1_bs512_noanim_20260518.log`, `logs/remote4090/momask_vq_load_preflight_20260518.log`, `logs/remote4090/soma30k_momask_mtrans_gpu1_20260518.log`, `logs/remote4090/soma30k_momask_rtrans_gpu1_20260518.log`, `logs/remote4090/soma30k_momask_eval_soma_hml3d_gpu1_20260519.log`, `logs/remote4090/soma30k_mogents_vq_gpu0_20260518.log`
- evaluator: `remote4090_full_conversion_gate; MoGenTS eval loader smoke; MoGenTS VQ monitor; MoMask sync preflight; MoMask VQ completion/checkpoint preflight; MoMask masked/residual transformer completion; MoMask eval_t2m_trans_res.py official generation eval`
- protocol: `30k 20fps HumanML3D-263 conversion completion check; clean_min40 split filter and Mean/Std recomputation; MoGenTS run_rvq monitor on GPU0; MoMask code sync, 29998 split loader gate, train_vq completion check, RVQVAE checkpoint load preflight, train_t2m_transformer/train_res_transformer completion on GPU1, and 20-repeat eval_t2m_trans_res.py on SOMA test and HumanML3D test`
- data_source: `soma30k_hml3d_full20fps_20260517.log + clean_min40_report.json + soma30k_mogents_eval_loader_smoke_20260518.log + soma30k_mogents_vq_gpu0_20260518.log + momask_setup_preflight_20260518.log + momask_loader_gate_20260518.log + soma30k_momask_vq_gpu1_retry_20260518.log + soma30k_momask_vq_gpu1_bs512_20260518.log + soma30k_momask_vq_gpu1_bs512_noanim_20260518.log + momask_vq_load_preflight_20260518.log + soma30k_momask_mtrans_gpu1_20260518.log + soma30k_momask_rtrans_gpu1_20260518.log + soma30k_momask_eval_soma_hml3d_gpu1_20260519.log + soma_test_latest_cs4_ts10_rep20_20260519.log + hml3d_test_latest_cs4_ts10_rep20_20260519.log + momask_env_mocritique_probe_20260518.log`
- condition_pair: `soma30k_full_conversion -> clean_min40_training_view`
- n/evaluable: `29998/30000 converted rows; 29991/29998 clean finite samples after min_len filtering; MoGenTS split=29991 and effective VQ train motions=20480; MoMask split=29998 and effective VQ train motions=20480; MoMask VQ/masked/residual completed; MoMask eval n=3000/3000 SOMA test and 4384/4384 HumanML3D test; MoGenTS VQ running at about 48%`
- coverage: raw BVH text-motion dataset construction, full HumanML3D-263 conversion, clean train/val/test split, MoGenTS eval loader smoke, MoGenTS VQ through about 48%, MoGenTS ckpt/animation existence and mp4 probe, MoMask code sync, loader gate, VQ completion/preflight, masked/residual transformer completion, and official SOMA/HumanML3D eval
- role: `cross_check`
- used_for: `observation`
- limitations: MoGenTS VQ 尚未完成；clean_min40 过滤会改变原始 30k selection 的 train count；MoMask 使用 full 29998 split 但 VQ loader 会按窗口长度形成有效训练 motion 子集；MoMask VQ/mtrans/rtrans 使用 `--eval_every_e 999` 避免训练中 mp4 保存失败，需要 checkpoint 后单独做可视化；MoMask eval 是 cross-check，不是 held-out final evaluator；KIMODO 指标来自不同 evaluator 和数据分布，不能作为 formal ordering evidence。
