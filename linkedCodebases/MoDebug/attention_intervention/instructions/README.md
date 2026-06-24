# Instructions

本目录保存运行指令和历史 handoff。历史文件保留原始运行语境，不作为结果聚合面。

| 文件 | 内容 |
|---|---|
| [handoff_history.md](handoff_history.md) | 原始 4090 dual-GPU handoff 与早期修复记录。 |

最终结果入口：

- [../results/summary.md](../results/summary.md)
- [../audit/auditability.md](../audit/auditability.md)
- [../visualization/README.md](../visualization/README.md)

后续若新增实验，应先补 source data，再重跑：

```bash
python3 linkedCodebases/MoDebug/attention_intervention/visualization/build_attention_visualizations.py
python3 linkedCodebases/MoDebug/attention_intervention/visualization/build_ldo_dso_visualizations.py
```
