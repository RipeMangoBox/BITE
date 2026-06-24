# Next Session Prompt: TAMR Step 0 — Motion Repr + Text Encoder Selection

你现在继续 TAMR 的 Step 0 后续工作。

## 必读上下文

先阅读以下文件，理解当前状态后再动手：

1. `/home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/motion_repr_ablation_local_2026-04-18_serial/summary.md` — 单次 5-schema 串行实验的完整结果
2. `/data/Life Me/ResearchWY Vault/paperIDEAs/TAMR/2026-04-18_motion-repr-ablation-summary.md` — 实验总结
3. `/data/Life Me/ResearchWY Vault/paperIDEAs/TAMR/prompts/2026-04-17_motion-repr-exploration.md` — 原始需求（schema 语义描述已按真实实现更新）
4. `/data/Life Me/ResearchWY Vault/paperIDEAs/TAMR/2026-04-15_tamr-status-and-roadmap.md` — 项目路线图

## Current State

- 5 个 schema 的 single-run (seed=42) 本地串行训练 + test eval 已全部完成。
- 当前排名（PrimaryScore = (R@1_t2m + R@1_m2t + R@5_t2m + R@5_m2t) / 4）：

| Rank | Schema | Dim | PrimaryScore | 备注 |
|------|--------|-----|--------------|------|
| 1 | `kimodo_like_261` | 261 | 14.16 | position + velocity + rotation + foot contact |
| 2 | `pos66` | 66 | 14.05 | 纯 global joint positions，最简单 |
| 3 | `guo263` | 263 | 13.37 | HumanML3D 标准特征 |
| 4 | `hy201_recon` | 201 | 13.03 | IK 重建的 local rotation + local position |
| 5 | `smpl_d135_recon` | 135 | 11.84 | IK 重建的纯 rotation |

- schema 语义以代码真实实现为准（见 exploration 文档第 102-110 行），不是最初 prompt 的旧描述。
- 本地已有 3 个预训练 T5 text encoder（`MotionPatches-main/pretrained_models/` 下）：

| Model | d_model | 来源 | 使用该模型的代表论文 |
|-------|---------|------|---------------------|
| `t5-base` | 768 | `t5-base` | Shape My Moves, FineMotion, MG-MotionLLM |
| `t5-large` | 1024 | `t5-large` | MoLingo |
| `flan-t5-base` | 768 | `google/flan-t5-base` | MotionGPT, HOIGPT, MoCHA |

- 当前 ablation 使用 `distilbert-base-uncased` (768d) 作为 frozen text encoder。

## 核心判断

1. `kimodo_like_261` 只比 `pos66` 高 0.11，单次 run 无法区分真实优势还是随机波动。需要多 seed 验证。
2. Text encoder 的选择是与 motion repr 正交的变量。当前只用了 DistilBERT，但 motion-text 领域主流已转向 T5 系列。应在固定 motion repr 后，再做 text encoder ablation，确保 Step 0 输出的是最优 (motion_repr, text_encoder) 组合。

## Your Task — 严格按优先级执行

### P0: Motion Repr 多 seed 验证

#### 1. 实验方案

对 `kimodo_like_261` 和 `pos66` 执行多 seed 验证：

- seed 列表：`[42, 43, 44, 45, 46]`（5 seeds）
- seed=42 已有结果，可直接复用（copy metrics.json + best_model.pt 到新目录结构）
- 实际需要新跑：每个 schema 4 runs，共 8 runs
- 输出目录结构：
  ```
  RUN_DIR/motion_repr_multiseed/
  ├── kimodo_like_261/
  │   ├── seed42/   ← 从已有结果 copy
  │   ├── seed43/
  │   ├── seed44/
  │   ├── seed45/
  │   └── seed46/
  ├── pos66/
  │   ├── seed42/   ← 从已有结果 copy
  │   ├── ...
  │   └── seed46/
  ├── multiseed_comparison.json
  └── decision_motion_repr.md
  ```

#### 2. 实现要求

- 写一个 `scripts/run_motion_repr_multiseed.py`（或修改现有脚本），支持在**同一进程内**循环多个 seed
- 关键：共享 `DistilBertTokenCache` 实例，避免每个 seed 重新加载 DistilBERT + 重建 ~70k caption 缓存（否则每次浪费 2-3 分钟）
- 每个 seed 独立 `seed_everything()` → 重新初始化 model + optimizer → 训练 → eval
- 命令行接口示例：
  ```bash
  python scripts/run_motion_repr_multiseed.py \
    --schemas kimodo_like_261 pos66 \
    --seeds 42 43 44 45 46 \
    --output-dir RUN_DIR/motion_repr_multiseed \
    --reuse-seed42-from RUN_DIR/motion_repr_ablation_kimodo_like_261 RUN_DIR/motion_repr_ablation_pos66
  ```
- 最终输出 `multiseed_comparison.json`，包含：
  - 每个 schema × 每个 seed 的完整 metrics
  - 每个 schema 的跨 seed mean ± std（PrimaryScore, t2m/R01, m2t/R01, t2m/R05, m2t/R05）

#### 3. Motion Repr 判定标准（写入 decision_motion_repr.md）

1. 比较 PrimaryScore 的 5-seed mean
2. 如果 mean 差距 > 1.0 → 选 mean 更高的
3. 如果 mean 差距 ≤ 1.0 → 选 `pos66`
   - 理由：维度更低（66 vs 261），训练/推理更快，可解释性更强
   - 在浅层 2-layer baseline 上，velocity/rotation 的冗余信息增益有限；后续 `TemporalSegmentEncoder` 可以从 position 序列隐式学到 velocity
   - `pos66` 与 MotionPatches 原始输入一致（`new_joints/` flatten），便于对比
4. 辅助参考 `t2m/R01` 和 `m2t/R01` 的 mean，确认两个方向没有严重偏科

### P0.5: Text Encoder Ablation（P0 完成、motion repr 固定后）

#### 1. 目的

在固定 motion repr 的前提下，对比 4 个 frozen text encoder，选出最优 text backbone。这样 Step 0 的最终输出是确定的 **(motion_repr, text_encoder)** 组合。

#### 2. 候选 text encoder

| ID | Model | d_model | 本地路径 |
|----|-------|---------|---------|
| `distilbert` | distilbert-base-uncased | 768 | HuggingFace cache（已有） |
| `t5-base` | t5-base (encoder only) | 768 | `MotionPatches-main/pretrained_models/t5-base/` |
| `t5-large` | t5-large (encoder only) | 1024 | `MotionPatches-main/pretrained_models/t5-large/` |
| `flan-t5-base` | google/flan-t5-base (encoder only) | 768 | `MotionPatches-main/pretrained_models/flan-t5-base/` |

#### 3. 实现要求

- 将 `DistilBertTokenCache` 泛化为 `TextEncoderCache`，支持 DistilBERT 和 T5 系列
  - T5 使用 `T5EncoderModel`（encoder-only），与 MotionPatches 的 `clip.py` 中 `_ENCODER_ONLY_MODEL_CLASS_BY_TYPE` 一致
  - 所有模型 frozen，不参与训练
  - 缓存逻辑不变：caption string → token embeddings
- `MotionReprBaseline` 的 `text_input_dim` 参数化：768 for distilbert/t5-base/flan-t5-base，1024 for t5-large
- 对 P0 选定的 motion schema，跑 4 个 text encoder × 3 seeds（seed=42,43,44，够用了因为这里只是选 text encoder）
- 输出目录结构：
  ```
  RUN_DIR/text_encoder_ablation/
  ├── distilbert/
  │   ├── seed42/ seed43/ seed44/
  ├── t5-base/
  │   ├── seed42/ seed43/ seed44/
  ├── t5-large/
  │   ├── seed42/ seed43/ seed44/
  ├── flan-t5-base/
  │   ├── seed42/ seed43/ seed44/
  ├── multiseed_comparison.json
  └── decision_text_encoder.md
  ```

#### 4. Text Encoder 判定标准

1. 比较 PrimaryScore 的 3-seed mean
2. 如果 top-1 和 top-2 的 mean 差距 ≤ 0.5 → 选参数量更小的（DistilBERT 66M < t5-base 220M < flan-t5-base 220M < t5-large 770M）
3. 如果 t5-large 显著优于其他（mean 差距 > 1.0），则选 t5-large，接受更高的推理开销
4. 注意：t5-large 的 d_model=1024，会改变 text-side `GlobalSequenceEncoder` 的 `input_proj` 维度，但 `latent_dim` 不变（仍为 256），所以 motion 侧权重可以复用

#### 5. decision_text_encoder.md 模板

```markdown
# Step 0.5 Decision: Text Encoder

## Fixed Motion Repr
- schema: `???` (from P0 decision)
- motion_input_dim: ???

## Multi-Seed Results (3 seeds: 42-44)

| Text Encoder | d_model | PrimaryScore (mean±std) | t2m/R01 | m2t/R01 |
|-------------|---------|------------------------|---------|---------|
| distilbert | 768 | ... | ... | ... |
| t5-base | 768 | ... | ... | ... |
| t5-large | 1024 | ... | ... | ... |
| flan-t5-base | 768 | ... | ... | ... |

## Decision

选定 text encoder: `???`
text_input_dim: ???

理由: ...
```

### P1: 输出最终 Step 0 Decision（P0 + P0.5 都完成后）

生成 `RUN_DIR/step0_final_decision.md`，包含：

```markdown
# TAMR Step 0 Final Decision

## 选定组合
- Motion representation: `???` (dim=???)
- Text encoder: `???` (d_model=???)
- text_input_dim: ???
- motion_input_dim: ???

## 后续 Structured Matching 阶段应使用
- motion 数据目录: `motion_formats/???/`
- normalization stats: `motion_format_stats/???/Mean.npy`, `Std.npy`
- text encoder 本地路径: `???`
- text encoder class: `???`（DistilBertModel 或 T5EncoderModel）

## 实验证据摘要
- Motion repr ablation: 5 schemas × 5 seeds, 选定 ??? (PrimaryScore mean=???)
- Text encoder ablation: 4 encoders × 3 seeds, 选定 ??? (PrimaryScore mean=???)
```

同时更新：
1. `2026-04-17_motion-repr-exploration.md` 的进度表
2. `2026-04-18_motion-repr-ablation-summary.md`

### P2: 工程清理（不阻塞 P0/P0.5/P1）

- 确认 `RUN_DIR/` 在 `.gitignore` 中
- 检查输出目录是否有多余嵌套层
- shell 脚本组织如有需要可顺手规范

## 约束

- 严格按 P0 → P0.5 → P1 → P2 顺序执行，不要跳步
- P0 和 P0.5 是两个独立的 ablation，不要同时变 motion repr 和 text encoder
- 不要修改已有的 single-run 结果文件
- 不要改动 `build_humanml3de_mp_motion_formats.py` 或 `build_motion_format_stats.py`
- 代码规范：嵌套 ≤ 4 层，类型注解，docstring 简洁
- 所有 seed/schema/text_encoder 共享同一个 text encoder cache 实例（同一进程内）
- T5 模型优先从本地 `MotionPatches-main/pretrained_models/` 加载，不要重新下载

## Output Preference

- 先给结论，再给理由，再给执行步骤
- 需要改代码/写脚本就直接实施，不要只写建议
