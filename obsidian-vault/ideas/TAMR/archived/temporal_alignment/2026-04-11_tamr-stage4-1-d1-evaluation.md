# TAMR Stage4.1 D1 评测结果

日期：2026-04-11

## 1. 评测执行

- 训练目录：`RUN_DIR/stage4_1_d1`
- checkpoint：`RUN_DIR/stage4_1_d1/tmr_d1_humanml3d_e_None/version_0/checkpoints/last.ckpt`
- 提取权重：`RUN_DIR/stage4_1_d1/last_weights/*.pt`
- 检索评测命令：

```bash
PYTHONPATH=. conda run -n TMR python retrieval.py \
  run_dir=RUN_DIR/stage4_1_d1 protocol=all batch_size=128 device=cuda ckpt=last
```

## 2. D1 训练期信号（核心）

来自 TensorBoard epoch 标量（100 epoch）：

- `train_evt_align`: `3.6119 -> 0.9288`（显著下降）
- `val_evt_align`: `3.2866 -> 2.0884`（下降）
- `train_evt_align_acc`: `0.1053 -> 0.8288`（显著上升）
- `val_evt_align_acc`: `0.1118 -> 0.3587`（上升，峰值 `0.3960`）

同时：

- `val_global` 基本恒定：`2.5697 -> 2.5697`
- `val_t2m/m2t` 检索指标在训练期几乎不变（和 frozen 设定一致）

结论：在 frozen feature 下，minimal event-time head 能提取到可学习的 event-time 信号（弱正信号成立）。

## 3. 检索评测结果（test）

产物目录：`RUN_DIR/stage4_1_d1/contrastive_metrics/`

### normal.yaml

- `t2m/R01`: `9.46`
- `t2m/R05`: `22.97`
- `t2m/R10`: `27.70`
- `m2t/R01`: `2.70`
- `m2t/R05`: `13.51`
- `m2t/R10`: `14.19`

### threshold_0.95.yaml

- `t2m/R01`: `16.22`
- `t2m/R05`: `27.03`
- `t2m/R10`: `31.76`
- `m2t/R01`: `3.38`
- `m2t/R05`: `13.51`
- `m2t/R10`: `14.19`

### nsim.yaml

- 当前使用 `nsim-like` 子集（`100/148`），构造方式：在 test 内按 sentence embedding 最近邻相似度筛选高相似样本（`min_sim=0.75`，top-100）
- `t2m/R01`: `13.00`
- `t2m/R05`: `29.00`
- `t2m/R10`: `37.00`
- `m2t/R01`: `3.00`
- `m2t/R05`: `12.00`
- `m2t/R10`: `18.00`

### guo.yaml

- `t2m/R01`: `18.75`
- `t2m/R05`: `41.41`
- `t2m/R10`: `56.25`
- `m2t/R01`: `9.38`
- `m2t/R05`: `28.12`
- `m2t/R10`: `42.97`

## 4. D1 阶段结论

- D1 的关键问题“冻结特征里是否存在可提取 event-time signal”得到**肯定**证据。
- global retrieval 在 frozen 设定下基本不动，符合 D1 设计预期。
- 下一步应进入 `D1.5`（uniform pooling control），验证 attention 本身是否带来额外价值。

## 5. 评测口径注意事项

- 当前 D1 检索池为 HumanML3D-E test（`len=148`），不可与完整 HumanML3D test（`len=4384`）的绝对 R@K 直接横向比较。
- `train_evt_align_acc` 与 `val_evt_align_acc` 有明显 gap（`0.8288` vs `0.3587`），后续 D1.5 / D2 应保持相同训练预算与更保守正则策略，避免不公平对比或过拟合放大。
