# trace_adapters — 模型特定 forward trace adapter

对每个 baseline 模型，在指定的内部层挂载 hook，用固定随机状态跑一次 forward，
将 hook 输出按 trace IO contract 格式写入 NPZ。

## 文件

| 文件 | 适配的模型族 | hook 位置 |
|------|------------|----------|
| `t5_trace_adapter.py` | T5-based (MotionGPT, MoLingo) | decoder prefix / latent AR state |
| `clip_discrete_trace_adapter.py` | CLIP discrete (MoMask, MoGenTS) | mask iteration codebook logits |

## 输出

每次调用产生一个 `forward_manifest.jsonl` + 一个 `{run_id}.npz`，包含:
- `signal`: 实际 hook 张量值
- `valid_mask`: 有效位置 mask（某些模型的部分位置在 hook 步未激活）
- `meta_json`: 运行元信息（model, sample_id, z_kind, condition_id ...）
- `axis_names_json`: 各维度的语义名称
