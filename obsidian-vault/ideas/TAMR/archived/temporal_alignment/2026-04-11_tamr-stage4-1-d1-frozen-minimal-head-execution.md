---
created: 1970-01-01T08:00
updated: 2026-04-11T14:35
---
# TAMR Stage4.1 D1 执行记录（frozen minimal event-time head）

日期：2026-04-11

## 1. 本次已落地内容

已在 TMR 代码库中新增 D1 最小实现：

- 冻结 backbone（`motion_encoder`）
- 冻结 text encoder（`text_encoder`）
- 仅训练最小 event-time head（`event_proj_e`, `event_proj_t`）
- 采用 `time-only` attention
- 采用固定口径 `masked InfoNCE`（跨样本 event 为负例，同样本其他 event 不作负例）

对应代码：

- `src/model/tmr_d1.py`
- `src/data/humanml3de_event.py`
- `src/data/collate.py`（新增 `collate_text_motion_event`）
- `src/model/actor.py`（支持返回 temporal hidden states）
- `configs/model/tmr_d1.yaml`
- `configs/data/humanml3d_e.yaml`
- `scripts/run_stage4_1_d1.sh`

## 2. D1 口径对齐说明

- warm-start：默认从 `models/tmr_humanml3d_guoh3dfeats/last_weights` 读取 encoder/decoder 权重
- frozen 设定：通过 `requires_grad=False` + 强制 `eval()` 固定冻结分支
- event-time attention：
  - `S_content(k,t)=<W_e E_k, W_t H_bar[t]>`
  - `A_time=softmax_t(S_content)`
  - `Z_k=sum_t A_time(k,t) * H_bar[t]`
- `masked InfoNCE`：
  - 正例 `(i, i)`
  - 负例仅跨样本 event
  - 同样本其他 event 被 mask，不参与负例
- loss：`L = λ_global * L_global + λ_evt_align * L_evt_align`
  - 默认 `λ_global=0.1, λ_evt_align=1.0`

## 3. 已执行的 smoke 验证

已跑通 1 train batch + 1 val batch（CPU smoke）：

```bash
conda run -n TMR python train.py \
  model=tmr_d1 data=humanml3d_e \
  run_dir=RUN_DIR/stage4_1_d1_smoke3 \
  dataloader.batch_size=4 dataloader.num_workers=0 \
  trainer.max_epochs=1 trainer.accelerator=cpu trainer.devices=1 \
  +trainer.limit_train_batches=1 +trainer.limit_val_batches=1
```

关键结果（epoch 0）：

- `train_loss`: `1.740e+00`
- `val_loss`: `1.699e+00`
- `train_global`: `9.638e-01`
- `val_global`: `1.458e+00`
- `train_evt_align`: `1.644e+00`
- `val_evt_align`: `1.553e+00`
- `train_evt_align_acc`: `0.4286`
- `val_evt_align_acc`: `0.4000`

产物目录：

- `RUN_DIR/stage4_1_d1_smoke3/`

## 4. 正式 D1 运行命令

```bash
bash scripts/run_stage4_1_d1.sh
```

可覆盖参数示例：

```bash
bash scripts/run_stage4_1_d1.sh trainer.max_epochs=50 dataloader.batch_size=32
```

## 5. 审查后修复（P0 / P1）

- `P0` 已修复：`_masked_event_infonce` 中 pooling 与对比统一到投影空间  
  - 从 `attn` 对 `motion_temporal` pooling 改为对 `proj_temporal` pooling  
  - 对比从 `event_latents` 改为 `proj_event`
- 修复后 smoke（CPU）已通过：
  - `run_dir=RUN_DIR/stage4_1_d1_smoke_p0fix`
  - `val_loss=1.382e+00`, `train_loss=1.685e+00`
- `P1` 已确认：GPU 路径可跑通（`used: True`）：
  - `run_dir=RUN_DIR/stage4_1_d1_gpu_smoke`
