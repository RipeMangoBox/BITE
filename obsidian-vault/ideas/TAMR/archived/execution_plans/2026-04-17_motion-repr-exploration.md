# GPT Prompt: Motion Representation Exploration (TAMR Step 0)

## 当前进度（2026-04-18）

| 项目 | 状态 | 备注 |
|------|------|------|
| `HumanML3D-E-MP` 单目录数据 | 已完成 | `new_joints/`、`texts/`、`train/val/test.txt` 已就绪 |
| `motion_formats/` 导出 | 已完成 | 5 个 schema 全量导出完成 |
| `motion_format_stats/` 统计 | 已完成 | 5 个 schema 的 `Mean.npy` / `Std.npy` 已生成 |
| ablation 代码实现 | 已完成 | Dataset / Model / Train script / shell scripts 已实现 |
| 本地单次 5-schema 串行实验 | 已完成 | train + best ckpt + test eval 已全部完成 |
| Step 0 最终 schema 固定 | 待确认 | 仍需优先比较 `kimodo_like_261` vs `pos66` 的多 seed 结果 |

## 当前实验结果（single-run local serial）

| Rank | Schema | 维度 | PrimaryScore | 状态 |
|------|--------|------|--------------|------|
| 1 | `kimodo_like_261` | 261 | 14.16 | 已完成，当前单次最佳 |
| 2 | `pos66` | 66 | 14.05 | 已完成，与最佳差距 0.11 |
| 3 | `guo263` | 263 | 13.37 | 已完成 |
| 4 | `hy201_recon` | 201 | 13.03 | 已完成 |
| 5 | `smpl_d135_recon` | 135 | 11.84 | 已完成 |

> 说明：当前结果来自单次本地串行 run，不应直接等同于最终结论。Step 0 的下一优先级任务是补 `kimodo_like_261` vs `pos66` 的多 seed 验证。

## 角色

你是一个 PyTorch 研究工程师。请为 TAMR 项目实现 Motion 表示探索实验的代码。

## 项目背景

这是 motion-text retrieval 项目的 Step 0：在实现 structured matching 之前，先用最简单的 global contrastive baseline 对比 5 种 motion 表示，选出最优表示后固定。

### 为什么要做这一步

- MotionPatches baseline 使用 `new_joints/` (22×3=66d joint positions)，不是 guo263 (263d)
- 后续所有模块（temporal segment encoder、matching、loss）都依赖固定的 motion 表示
- 如果先做 structured matching 再换表示，所有实验需要重跑
- 本地无原生 SMPL rotation 文件，所有 rotation 均为 IK 重建，精度和 guo263 内部的 rot_data 等价

### 现有代码上下文

#### 已有的 motion format 导出脚本

`scripts/build_humanml3de_mp_motion_formats.py` 已实现 5 种 schema 的转换：
- 输入：`new_joints/` 目录下的 `(T, 22, 3)` joint position `.npy` 文件
- 输出：每种 schema 一个子目录，每个样本一个 `.npy` 文件
- 已实现的 schema：`guo263`, `pos66`, `smpl_d135_recon`, `hy201_recon`, `kimodo_like_261`

该脚本已经可以运行，不需要修改。

#### MotionPatches 的数据加载方式

MotionPatches 的 `TextMotionPatchDataset`：
- 从 `new_joints/` 加载 `(T, 22, 3)` 的 `.npy` 文件
- 用 `Mean_raw.npy` / `Std_raw.npy` (shape `(22, 3)`) 做 z-score normalization
- 然后用 `use_kinematic()` 将 5 条 kinematic chain 各插值到 16 点，reshape 成 `(3, T_pad, 80)` 伪图像送入 ViT
- 文本侧用 CLIP text encoder

kinematic chain 定义（HumanML3D）：
```python
[
    [0, 2, 5, 8, 11],     # right leg
    [0, 1, 4, 7, 10],     # left leg
    [0, 3, 6, 9, 12, 15], # torso
    [9, 14, 17, 19, 21],  # right arm
    [9, 13, 16, 18, 20],  # left arm
]
```

#### 现有 event_grounded 模块

`src/model/event_grounded/` 下已有：
- `EventTextEncoder`：接收 `[N, L, 768]` DistilBERT token embeddings → `[N, D]`
- `TemporalSegmentEncoder`：接收 `[B, T, input_dim]` motion features → `[B, S, D]`
- 两者内部都用 `nn.Linear(input_dim, latent_dim)` 做投影，对 motion 表示是 agnostic 的

#### 数据目录结构

```
datasets/
├── HumanML3D-E-MP/          # MotionPatches 格式的 HumanML3D-E 数据
│   ├── new_joints/           # (T, 22, 3) joint positions
│   ├── texts/                # 文本标注
│   ├── Mean_raw.npy          # (22, 3) normalization stats for pos66
│   ├── Std_raw.npy
│   ├── train.txt / val.txt / test.txt
│   └── data_{train,val,test}.npy  # packaged dict, motion=(T,263) guo format
├── HumanML3D/HumanML3D/
│   ├── joints/               # (T, 52, 3) raw AMASS positions
│   ├── new_joints/           # (T, 22, 3) uniform skeleton positions
│   ├── new_joint_vecs/       # (T, 263) guo features
│   ├── new_joints_abs_3d/    # (T, 22, 3) absolute root variant
│   ├── new_joint_vecs_abs_3d/ # (T, 263) absolute root variant
│   ├── Mean.npy / Std.npy    # (263,) stats for guo263
│   ├── Mean_raw.npy / Std_raw.npy  # (22, 3) stats for pos66
│   └── index.csv             # AMASS clip → HumanML3D ID mapping
```

## 5 种候选表示

| Schema | 维度 | 内容 | 进度 |
|--------|------|------|------|
| `guo263` | (T, 263) | root(4) + ric_pos(63) + rot_6d(126) + vel(66) + foot_contact(4) | 已完成 |
| `pos66` | (T, 66) | flatten 后的 22 joints × 3D global position | 已完成 |
| `smpl_d135_recon` | (T, 135) | root_6d(6) + root_xz_velocity(2) + root_height(1) + 21 joints × 6D cont rotation(126) | 已完成 |
| `hy201_recon` | (T, 201) | root_pos(3) + root_6d(6) + 21 joints × 6D local rotation(126) + 22 joints × 3D root-frame local position(66) | 已完成 |
| `kimodo_like_261` | (T, 261) | smoothed_root_pos(3) + heading_2d(2) + non_root_pos(63) + non_root_vel(63) + rot_6d(126) + foot_contact(4) | 已完成 |

> 注意：上表已经按当前代码真实实现同步更新，不再沿用最初 prompt 里对 `smpl_d135_recon`、`hy201_recon`、`kimodo_like_261` 的旧语义描述。

## 需要实现的模块

### 1. `scripts/build_motion_format_stats.py`

进度：已完成

为每种 schema 计算 per-dimension Mean 和 Std normalization stats。

输入：
- `--format-root`：`build_humanml3de_mp_motion_formats.py` 的输出目录，结构为 `{format_root}/{schema}/000021.npy`
- `--schemas`：要处理的 schema 列表，默认全部 5 种
- `--split-file`：train split 文件路径（只用 train set 计算 stats）
- `--output-dir`：输出目录

输出：
- `{output_dir}/{schema}/Mean.npy`：shape `(D,)` 的 per-dimension mean
- `{output_dir}/{schema}/Std.npy`：shape `(D,)` 的 per-dimension std（clip min=1e-6 避免除零）

注意：
- `pos66` 的 motion format 文件当前按 `(T, 66)` 保存；实现里仍兼容 `(T, 22, 3)` 输入并会自动 reshape
- 其他 schema 的输入文件已经是 `(T, D)` 格式
- stats 应该在所有 train samples 的所有 frames 上计算（concatenate all frames then compute）

### 2. `src/data/motion_repr_dataset.py`

进度：已完成

支持多种 motion 表示的 PyTorch Dataset 类。

```python
class MotionReprDataset(torch.utils.data.Dataset):
    """
    通用 motion-text dataset，支持多种 motion 表示 schema。
    用于 motion representation ablation 实验。
    """
```

设计要求：
- `__init__` 参数：
  - `motion_dir: str` — 某个 schema 的 motion 文件目录
  - `text_dir: str` — 文本标注目录
  - `split_file: str` — split 文件路径
  - `mean_path: str` — Mean.npy 路径
  - `std_path: str` — Std.npy 路径
  - `max_motion_length: int = 224`
  - `text_encoder: str = "distilbert"` — 预留，当前只用 distilbert
- 数据加载：
  - motion：加载 `.npy`，如果 shape 是 `(T, J, 3)` 则 reshape 为 `(T, J*3)`，z-score normalize
  - text：从 `{text_dir}/{name}.txt` 加载，每行格式为 `caption#tokens#f_tag#to_tag`，随机选一条 caption
  - 如果 motion 长度 > max_motion_length，随机裁剪；如果 < max_motion_length，zero-pad
- `__getitem__` 返回 dict：
  - `"motion"`: `(max_motion_length, D)` float32 tensor
  - `"motion_length"`: int
  - `"caption"`: str
  - `"name"`: str（sample ID）
- collate_fn：标准 default_collate 即可（motion 已 pad 到同一长度）

### 3. `src/model/motion_repr_baseline.py`

进度：已完成

用于 motion representation ablation 的 global contrastive baseline 模型。

```python
class MotionReprBaseline(nn.Module):
    """
    最简单的 global contrastive motion-text retrieval baseline。
    Motion encoder: Linear projection + Transformer + mean pool → [B, D]
    Text encoder: DistilBERT frozen embeddings + Transformer + mean pool → [B, D]
    Loss: symmetric InfoNCE
    """
```

设计要求：
- `__init__` 参数：
  - `motion_input_dim: int` — 根据 schema 变化（66/135/201/261/263）
  - `text_input_dim: int = 768` — DistilBERT hidden dim
  - `latent_dim: int = 256`
  - `num_layers: int = 2`
  - `num_heads: int = 4`
  - `ff_size: int = 512`
  - `dropout: float = 0.1`
  - `temperature: float = 0.07`
- Motion encoder：
  - `nn.Linear(motion_input_dim, latent_dim)` → positional encoding → `nn.TransformerEncoder(num_layers)` → mean pool (masked) → `[B, D]`
- Text encoder：
  - `nn.Linear(text_input_dim, latent_dim)` → positional encoding → `nn.TransformerEncoder(num_layers)` → mean pool (masked) → `[B, D]`
- `forward(motion, motion_length, text_emb, text_length)` → loss dict
- `encode_motion(motion, motion_length)` → `[B, D]`
- `encode_text(text_emb, text_length)` → `[B, D]`
- Loss：标准 symmetric InfoNCE，和 `EventGroundedContrastiveLoss` 中的实现一致

注意：
- Text 侧需要先用 DistilBERT 提取 token embeddings。为了简化，可以在 Dataset 中预计算并缓存，或者在 model 中 lazy load DistilBERT（frozen，不参与训练）
- 推荐方案：model 内部持有 frozen DistilBERT，forward 时接收 raw text string，内部 tokenize + encode。这样 Dataset 只需要返回 caption string

### 4. `scripts/run_motion_repr_ablation.py`

进度：已完成

自动化 5 种表示的训练+评估 pipeline。

设计要求：
- 命令行参数：
  - `--schemas`：要跑的 schema 列表，默认全部 5 种
  - `--format-root`：motion format 数据根目录
  - `--stats-root`：normalization stats 根目录
  - `--text-dir`：文本标注目录
  - `--split-dir`：包含 train.txt/val.txt/test.txt 的目录
  - `--output-dir`：实验输出目录
  - `--epochs`：最大训练 epoch 数，默认 50
  - `--batch-size`：默认 32
  - `--lr`：默认 1e-4
  - `--device`：默认 cuda
  - `--seed`：默认 42
- 训练循环：
  - 标准 PyTorch 训练循环（不用 Lightning，保持简单）
  - Adam optimizer，cosine annealing scheduler
  - 每 epoch 在 val set 上评估 R@1，early stop（patience=10）
  - 保存 best checkpoint
- 评估：
  - 训练结束后，加载 best checkpoint，在 test set 上计算：
    - R@1, R@5, R@10, MedR（t2m 和 m2t 两个方向）
    - PrimaryScore = (R@1_t2m + R@1_m2t + R@5_t2m + R@5_m2t) / 4
  - 评估方式：encode 所有 test motion 和 test text，计算 cosine similarity matrix，排序
- 输出：
  - `{output_dir}/{schema}/best_model.pt`
  - `{output_dir}/{schema}/metrics.json`
  - `{output_dir}/comparison_table.json`：汇总所有 schema 的指标

### 5. `configs/experiment/motion_repr_ablation.yaml`

进度：已完成

Hydra config 片段（供参考，实际训练脚本不依赖 Hydra）：

```yaml
defaults:
  - _self_
schemas:
  - guo263
  - pos66
  - smpl_d135_recon
  - hy201_recon
  - kimodo_like_261
schema_dims:
  guo263: 263
  pos66: 66
  smpl_d135_recon: 135
  hy201_recon: 201
  kimodo_like_261: 261

training:
  epochs: 50
  batch_size: 32
  lr: 1.0e-4
  weight_decay: 1.0e-5
  patience: 10
  seed: 42

model:
  latent_dim: 256
  num_layers: 2
  num_heads: 4
  ff_size: 512
  dropout: 0.1
  temperature: 0.07

data:
  text_dir: ${oc.env:MOTIONPATCHES_DATA_ROOT,../datasets/HumanML3D-E-MP}/texts
  split_dir: ${oc.env:MOTIONPATCHES_DATA_ROOT,../datasets/HumanML3D-E-MP}
  max_motion_length: 224
```

## 代码规范

- PyTorch，纯 nn.Module + 标准训练循环，不依赖 PyTorch Lightning
- 类型注解，docstring 简洁
- 嵌套层级不超过 4 层
- 所有 hyperparameters 通过参数传入
- 文件组织：
  - `scripts/build_motion_format_stats.py`
  - `src/data/motion_repr_dataset.py`
  - `src/model/motion_repr_baseline.py`
  - `scripts/run_motion_repr_ablation.py`
  - `configs/experiment/motion_repr_ablation.yaml`

## 输出要求

1. 输出上述 5 个文件的完整代码
2. 每个文件开头注明文件路径
3. 附一个简短的 smoke test 片段，验证 Dataset + Model 的 forward pass 能跑通（fake data）
4. 附运行说明：从 format 导出 → stats 计算 → 训练 → 评估的完整命令序列

## 重要约束

1. Text encoder 使用 DistilBERT（`distilbert-base-uncased`），frozen，不参与训练
2. Motion encoder 的架构必须和 `TemporalSegmentEncoder` 内部的 segment encoder 一致（Linear + PE + TransformerEncoder + mean pool），这样后续切换到 structured matching 时可以直接复用权重
3. 评估指标计算方式必须和 MotionPatches 的评估一致（cosine similarity matrix → rank）
4. 所有 schema 共享同一套 text embeddings，只有 motion 侧不同
5. 训练时 motion 和 text 是 batch 内一一对应的正样本对，batch 内其他样本为负样本
