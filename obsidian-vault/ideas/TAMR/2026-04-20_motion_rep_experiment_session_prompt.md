# HumanML3D-E-MP 多 Motion Rep 实验 — 新会话 Prompt

> [!warning]
> 这份 prompt 是 `HumanML3D-E-MP` motion-rep 实验时期的历史执行提示，不是当前 `linkedCodebases/TMR` `master` 分支的现行入口说明。当前本地 `TMR` 已还原到 `master`，其中并不存在本文引用的 `scripts/run_tmr_humanml3de_mp_*`、`configs/data/humanml3d_e_mp.yaml`、`configs/model/tmr_d2b_ft.yaml` 等分支期文件。若要按当前 `master` 使用 `TMR`，应以 `train.py`、`extract.py`、`retrieval.py`、`text_motion_sim.py` 和 `models/tmr_humanml3d_guoh3dfeats` 为准。

## 当前状态

guo263 闭环验证已通过。vanilla TMR 在 HumanML3D-E-MP guo263 上从零训练 15 epoch，指标正常上涨：

| Epoch | E-MP guo263 v_t2m/R01 | E-MP guo263 v_m2t/R01 | 原始TMR v_t2m/R01 | 原始TMR v_m2t/R01 |
|------:|----------------------:|----------------------:|------------------:|------------------:|
|     0 |                 1.37% |                 1.63% |             1.24% |             2.04% |
|     2 |                 3.33% |                 3.33% |             5.03% |             4.96% |
|     5 |                 5.42% |                 5.29% |             8.33% |             8.47% |
|    10 |                 7.58% |                 7.12% |            10.89% |            11.39% |
|    14 |                 9.22% |                 8.81% |            12.86% |            16.14% |

E-MP guo263 增速略慢于原始 TMR（约 0.7x），原因是：
- E-MP 的 guo263 由 MotionStreamer 的 hml272 格式重新计算，与原始 TMR 的 guoh3dfeats 数值分布不同（normalizer stats max_abs_diff=0.9）
- validation set 大小不同（E-MP: 1530 vs 原始: 1368），更大的 val set 会稍微压低 R@k
- 但趋势正常，确认数据管线无 bug

## 指标公平性确认

**已确认公平。** vanilla TMR 的 `on_validation_epoch_end`（`src/model/tmr.py:168`）用模型自己的 text_encoder 和 motion_encoder 产出 `t_latents` / `m_latents`，计算 sim_matrix 得到 retrieval 指标。不依赖任何外部预训练权重或冻结 latent。每种 motion rep 的指标完全基于该 rep 自身的训练状态。

## 实验方案

三条路线，每种 motion rep 都跑：

```
路线A: vanilla TMR 500ep（产出 warm-start）
  model=tmr, loss=recons+latent+kl+contrastive, 全模块训练, 无event信息
  → 产出 last_weights/ 作为路线B的warm-start

路线B: Finetune（D2b + P2a 都跑，各50ep）
  B1: model=tmr_d2b_ft, freeze_text_encoder=true, loss=global+evt_align
  B2: model=tmr_p2a_ft, freeze_text_encoder=false, loss=global+evt_align
  → warm_start_weights_dir 自动指向路线A产出

路线C: P2a scratch 500ep（不finetune路线）
  model=tmr_p2a_scratch, 从零训练, loss=global+evt_align, text+motion encoder全训
```

6种 motion rep: guo263, pos66, kimodo261, smpl135, hy201, hml272

## 已完成的代码修改

配置文件（均在 configs/model/）：
- `tmr_d2b_ft.yaml` — D2b finetune，warm_start 运行时注入
- `tmr_p2a_ft.yaml` — P2a finetune，warm_start 运行时注入
- `tmr_p2a_scratch.yaml` — P2a 从零训练

脚本（均在 scripts/）：
- `run_tmr_humanml3de_mp_motion_repr.py` — 支持 --stage warmstart/finetune_d2b/finetune_p2a/scratch/all
- `run_tmr_humanml3de_mp_gpu0.sh` — GPU0, schemas=(guo263 pos66 kimodo261)
- `run_tmr_humanml3de_mp_gpu1.sh` — GPU1, schemas=(smpl135 hy201 hml272)

## 当前 guo263 warmstart 训练状态

正在 GPU0 上跑 `model=tmr, epochs=20`（闭环测试）。
产出目录: `outputs/humanml3d_e_mp_motion_repr_server/tmr/guo263/`

## 下一步操作

### 步骤1: 等待当前 guo263 warmstart 闭环测试完成（20ep）

确认最终指标趋势正常后，删除闭环测试产出，开始正式实验。

### 步骤2: 启动正式实验（双卡并行）

guo263 的 warmstart 阶段已有部分 epoch，可以用 resume 继续；其他 rep 从零开始。

```bash
# 设置环境变量
unset HF_ENDPOINT
export HUMANML3DE_MP_ROOT=/home/ripemangobox/Coding/Github/Motion/datasets/HumanML3D-E-MP
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

# GPU0: guo263 + pos66 + kimodo261, 全部路线
nohup bash scripts/run_tmr_humanml3de_mp_gpu0.sh \
  --skip-retrieval \
  > outputs/humanml3d_e_mp_motion_repr_server/logs/gpu0_nohup.log 2>&1 &

# GPU1: smpl135 + hy201 + hml272, 全部路线
nohup bash scripts/run_tmr_humanml3de_mp_gpu1.sh \
  --skip-retrieval \
  > outputs/humanml3d_e_mp_motion_repr_server/logs/gpu1_nohup.log 2>&1 &
```

### 步骤3: 单独跑 scratch 路线（可选，与步骤2并行或之后）

```bash
# GPU0: scratch 路线
STAGE_OVERRIDE=scratch nohup bash scripts/run_tmr_humanml3de_mp_gpu0.sh \
  --skip-retrieval \
  > outputs/humanml3d_e_mp_motion_repr_server/logs/gpu0_scratch_nohup.log 2>&1 &

# GPU1: scratch 路线
STAGE_OVERRIDE=scratch nohup bash scripts/run_tmr_humanml3de_mp_gpu1.sh \
  --skip-retrieval \
  > outputs/humanml3d_e_mp_motion_repr_server/logs/gpu1_scratch_nohup.log 2>&1 &
```

### 步骤4: 训练完成后跑 retrieval evaluation

```bash
# 去掉 --skip-retrieval，或单独跑 retrieval.py
# 对每个 run_dir 执行 retrieval evaluation
```

## 关键文件索引

| 文件 | 用途 |
|------|------|
| `scripts/run_tmr_humanml3de_mp_motion_repr.py` | Python 入口，--stage 控制路线 |
| `scripts/run_tmr_humanml3de_mp_gpu0.sh` | GPU0 launcher |
| `scripts/run_tmr_humanml3de_mp_gpu1.sh` | GPU1 launcher |
| `configs/model/tmr.yaml` | 路线A: vanilla TMR |
| `configs/model/tmr_d2b_ft.yaml` | 路线B1: D2b finetune |
| `configs/model/tmr_p2a_ft.yaml` | 路线B2: P2a finetune |
| `configs/model/tmr_p2a_scratch.yaml` | 路线C: P2a scratch |
| `configs/data/humanml3d_e_mp.yaml` | 数据配置 |
| `configs/data/motion_loader/emp_*.yaml` | 各 motion rep 的 loader 配置 |

## 注意事项

1. **不要使用原始 TMR 的 warm-start 权重**（`models/tmr_humanml3d_guoh3dfeats/last_weights`）——E-MP 的 motion 数据分布与原始 TMR 不同，warm-start 会失效
2. **路线A（warmstart）默认 stage=all 会自动串行执行 warmstart → finetune_d2b → finetune_p2a**
3. **scratch 路线需要单独用 STAGE_OVERRIDE=scratch 启动**，不包含在 all 中
4. **batch_size=128, seed=1234, num_workers=8** 是默认配置，与原始 TMR baseline 对齐
5. 当前闭环测试用了 num_workers=0（为了调试），正式实验应使用默认的 8
