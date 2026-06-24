# Phase 0.5 任务 Prompt：在 ClipModel 框架下训练非 pos66 Motion Representations

## 目标

在 MotionPatches 的完整 `ClipModel` 框架（ViT-B/16 + DistilBERT，端到端微调）下，训练以下 motion representation 并与 pos66 baseline 做公平对比：

- `kimodo_like_261` (261d)
- `guo263` (263d)
- `hy201_recon` (201d)
- `smpl_d135_recon` (135d)
- `hml272` (272d) — 需要先生成数据

## 核心问题

当前 `TextMotionPatchDataset`（`datasets/dataset.py`）和 `MotionEncoder`（`models/clip.py`）只支持 `[T, J, 3]` 格式的 position-based motion（pos66 = 22 joints × 3 xyz）。非 pos66 的表示是 `[T, D]` 2D 格式，无法直接使用 `use_kinematic` 函数。

### 数据流（当前 pos66 路径）

```
np.load(motion_dir/name.npy)  →  [T, 22, 3]
  → normalize: (motion - Mean_raw[1,22,3]) / Std_raw[1,22,3]
  → use_kinematic: 按 5 条 kinematic chain 分组，每条 resize 到 16 点 → [T, 80, 3]
  → rearrange("t j c -> c t j") → [3, T, 80]
  → ViT patch_embed: Conv2d(3, 768, kernel_size=(16,16), stride=(16,16))
  → img_size=(224, 80) → 14×5=70 patches + 1 CLS token
```

### 需要实现的适配

对于 `[T, D]` 格式的 motion，需要一个新的数据加载和 patch 化路径：

1. **数据加载**：从 `motion_formats/{schema}/` 目录加载 `[T, D]` 格式的 npy 文件
2. **标准化**：使用 `motion_format_stats/{schema}/Mean.npy` 和 `Std.npy`（shape 为 `[D]`）
3. **Patch 化策略**：将 `[T, D]` 转为 ViT 可接受的 `[C, H, W]` 格式

## 关键文件

| 文件 | 作用 | 需要修改 |
|---|---|---|
| `datasets/dataset.py` | `TextMotionPatchDataset` 数据加载 + `use_kinematic` patch 化 | 是 |
| `models/clip.py` | `MotionEncoder`（timm ViT）+ `ClipModel` | 可能需要调整 `img_size` |
| `scripts/train.py` | 训练入口，加载 Mean/Std，构建 dataset | 是 |
| `conf/config.yaml` | Hydra 配置 | 需要新增 motion_format 相关配置 |

## 数据位置

- Motion formats: `../datasets/HumanML3D-E-MP/motion_formats/{schema}/{sample_id}.npy`
- Stats: `../datasets/HumanML3D-E-MP/motion_format_stats/{schema}/Mean.npy`, `Std.npy`
- Text: `../datasets/HumanML3D-E-MP/texts/` 或 `data/HumanML3D/texts/`
- Splits: `datasets/annotations/humanml3de/splits/{train,val,test}.txt`

各 schema 的数据 shape：
- `kimodo_like_261`: `[T, 261]`
- `guo263`: `[T, 263]`
- `hy201_recon`: `[T, 201]`
- `smpl_d135_recon`: `[T, 135]`
- `pos66`: `[T, 66]`（已有 `[T, 22, 3]` 格式在 `new_joints/`）

## Patch 化设计建议

### 方案：1D Temporal Patching

将 `[T, D]` 视为单通道 "image" `[1, T, D]`，用 1D temporal patching：

```
[T, D] → pad T to 224 → reshape to [1, 224, D]
→ ViT patch_embed: Conv2d(1, 768, kernel_size=(16, patch_w), stride=(16, patch_w))
```

其中 `patch_w` 需要根据 D 选择，使得 `D / patch_w` 为整数且 patch 数量合理。

或者更简单的方案：将 D 维度按语义分组（类似 kinematic chain），每组 resize 到固定宽度。

### 推荐方案：Linear Projection + 保持 ViT 结构

最简单且最通用的方案：

1. 在 `MotionEncoder` 前加一个 `nn.Linear(D, 22*3)` 将任意 D 维投影到 66 维
2. reshape 成 `[T, 22, 3]`，然后走原有的 `use_kinematic` 路径
3. 这样 ViT 的 `patch_embed` 和 `pos_embed` 都不需要改，pretrained 权重可以完整加载

缺点：线性投影可能丢失信息。但这是最小改动方案，且保证了与 pos66 baseline 的架构一致性。

### 替代方案：替换 patch_embed

1. 替换 ViT 的 `patch_embed.proj` 为 `Conv2d(1, 768, kernel_size=(16, D), stride=(16, D))`
2. 输入为 `[1, T_padded, D]`
3. 这样每个 patch 覆盖 16 帧 × 全部 D 维特征
4. `pos_embed` 需要重新初始化（因为 patch 数量变了）
5. pretrained ViT 的 `patch_embed` 和 `pos_embed` 权重无法使用，其余 Transformer blocks 可以保留

## 训练配置

与 `plain00_s42` 对齐：

```yaml
model:
  motion_encoder: vit_base_patch16_224_in21k
  text_encoder: distilbert-base-uncased
train:
  batch_size: 64
  epoch: 50
  optimizer:
    motion_lr: 1.0e-05
    text_lr: 1.0e-05
    head_lr: 1.0e-05
  train_motion_encoder: true
  train_text_encoder: true
  motion_encoder_pretrained: true
  patch_size: 16
  seed: 42
  dataset_regime: humanml3de
```

## pos66 Baseline 指标（参考）

| Experiment | t2m/R01 | m2t/R01 | t2m/R05 | m2t/R05 | t2m/MedR | m2t/MedR | eval_len |
|---|---|---|---|---|---|---|---|
| `exp1` (bs=128, original data) | 7.66 | 11.88 | 26.19 | 28.65 | 19.0 | 19.5 | 4384 |
| `plain00_s42` (bs=64, humanml3de) | 7.12 | 10.07 | 24.77 | 25.44 | 20.0 | 19.5 | 4646 |
| `ref00_s42` (bs=64, humanml3de) | 7.27 | 10.92 | 24.86 | 27.31 | 19.0 | 18.5 | 4196 |
| `ref00_s43` | 7.32 | 10.61 | 25.26 | 28.03 | 18.0 | 18.5 | 4196 |
| `ref00_s44` | 7.46 | 11.77 | 26.60 | 28.84 | 18.0 | 18.0 | 4196 |

## 实现步骤

1. **选择 patch 化方案**并实现（推荐 Linear Projection 方案，最小改动）
2. **修改 `TextMotionPatchDataset`**：支持从 `motion_formats/` 加载 `[T, D]` 数据，使用对应的 Mean/Std
3. **修改 `train.py`**：支持新的配置项（`motion_format_schema`），加载正确的 Mean/Std
4. **修改 `conf/config.yaml`**：新增 `dataset.motion_format_schema` 配置
5. **写训练脚本**：串行训练 5 个 schema，每个 50 epoch
6. **评估**：使用与 `ref00_s42` 相同的 eval 流程，输出 `contrastive_metrics/normal.yaml`

## hml272 数据生成

hml272 数据目前不在 `motion_formats/` 中。需要：
1. 运行 `scripts/build_humanml3de_mp_motion_formats.py --schemas hml272` 生成数据
2. 运行 `scripts/build_motion_format_stats.py` 生成 Mean/Std

## 注意事项

- 不要修改现有的 pos66 训练路径，新增一个并行路径
- 确保 eval 使用相同的 test split 和 eval 流程
- 所有实验使用 `dataset_regime: humanml3de`（HumanML3D-E 的 split）
- GPU: 使用 `gpu_id: 0` 或 `gpu_id: 1`（根据可用性）
- 每个实验的 checkpoint 保存到 `checkpoints/phase05_{schema}_s42/HumanML3D/`
