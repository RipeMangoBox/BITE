# Attention Intervention Experiment Pack

本目录是 4090 双卡 attention intervention 实验的整理面，替代旧的 `experiments/attention_intervention_*` 临时位置。

## 目录结构

| 目录 | 用途 |
|---|---|
| `instructions/` | 运行指令、历史 handoff、远程 tmux/log/check 命令。 |
| `audit/` | 可审计性矩阵、证据口径、未完成项和风险说明。 |
| `results/` | 综合报告和每个 baseline 的独立结果报告。 |
| `visualization/` | 零依赖 Python 可视化脚本、结构化 CSV、生成的 SVG 图。 |

## 阅读顺序

1. [results/summary.md](results/summary.md)：一次性看完成矩阵、审计矩阵和主要结果。
2. [audit/auditability.md](audit/auditability.md)：看每个 baseline 的可审计性和限制。
3. [results/motionclr.md](results/motionclr.md)、[results/motiongpt.md](results/motiongpt.md)、[results/molingo.md](results/molingo.md)：看 baseline 内细节。
4. [visualization/README.md](visualization/README.md)：重生成 CSV 和图。

机制讨论入口：
[results/data_analysis_and_mechanism_discussion_20260609.md](results/data_analysis_and_mechanism_discussion_20260609.md)。
