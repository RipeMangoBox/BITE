# trace_metrics — delta 计算与 contract 校验

## 文件

| 文件 | 职责 |
|------|------|
| `compute_delta.py` | 对配对的 text/null_text forward NPZ 计算逐元素 delta，输出 delta NPZ |
| `trace_contract_validator.py` | 校验 forward/delta NPZ 是否符合 IO contract（必需 key、shape 一致性、manifest 完整性） |

## Delta 计算

```
delta = forward(text_condition="text") − forward(text_condition="null_text")
```

在完全相同的随机状态下计算。delta NPZ 额外包含:
- `metric_value`: relative_l2 = ||delta|| / ||forward(text)||
- `valid_mask`: 从 forward NPZ 传播的有效位置 mask
- `axis_names_json`: 与 forward 一致的维度名
