---
title: "L40 文本编码器实验准备状态"
created: 2026-05-17T18:52:07+08:00
updated: 2026-05-20T13:45:48+08:00
type: infrastructure_status
tags:
  - MoDebug
  - L40
  - text_embedding
---

# L40 文本编码器实验准备状态

## 目标

为 P1 text-side diagnostic 扩展准备 L40 远程执行环境，用 T5 多权重、Qwen32B 和 DistilBERT 复查 P1 full-vs-single 文本侧相似度与距离趋势。

## 数据对象

- 远程 host：`L40`，SSH alias 已存在。
- 远程工作目录：`/sata/public/ripemangobox/Motion`。
- GPU：`2 x NVIDIA L40`。
- 本地 MCP 源码：`/home/ripemangobox/mcp/remoteL40`。
- Codex MCP 注册：`/home/ripemangobox/.codex/config.toml` 中新增 `[mcp_servers.remoteL40]`。

## 计算方式

复用 `remote4090` MCP 的受限 SSH/tmux/rsync 工作流，独立生成 `rl40_*` 工具名前缀，默认远程目录设为 `/sata/public/ripemangobox/Motion`。通过 `uv --directory /home/ripemangobox/mcp/remoteL40 run python` 直接调用 `rl40_status()` 做本地 smoke。

## 当前结论

- L40 SSH 连通，`tmux`、`rsync`、`git`、`nvidia-smi` 可用。
- `remoteL40` MCP 代码已创建并通过 `py_compile`。
- `rl40_status()` 直接函数调用通过，可返回 L40 双卡状态。
- 当前 Codex 会话不会自动出现新 MCP 工具；需要新会话或 MCP reload 后才会出现 `mcp__remoteL40__...` 工具。
- T5 权重同步已完成：本地 `t5-base`、`t5-large`、`google/flan-t5-base` 已 rsync 到 `/sata/public/ripemangobox/Motion/text_encoders/hf_cache/hub/`。
  - `t5-base`: `853M`
  - `t5-large`: `2.8G`
  - `google/flan-t5-base`: `948M`
- Qwen32B 独立 Python 环境已创建：`/sata/public/ripemangobox/Motion/envs/qwen32b`。
- 环境 smoke 已通过：`huggingface_hub 1.15.0`、`transformers 5.8.1`、`accelerate 1.13.0`、`safetensors 0.7.0`、`tokenizers 0.22.2`。
- `torch 2.12.0+cu130` 与 L40 CUDA 12.2 driver 不兼容，已替换为 `torch 2.5.1+cu121`；`torch.cuda.is_available=True`，双 L40 可见。
- Qwen32B 权重下载已完成：
  - model_id: `Qwen/Qwen3-32B`
  - local_dir: `/sata/public/ripemangobox/Motion/llm_cache/Qwen3-32B`
  - cache_dir: `/sata/public/ripemangobox/Motion/llm_cache/hub`
  - log: `/sata/public/ripemangobox/Motion/logs/qwen32b_download_20260517.log`
- final observed: `56` files, `65540301822` bytes, local dir about `62G`.
- Text embedding ext 已完成：
  - run: `run_20260517_l40_multiscale`
  - remote output: `/sata/public/ripemangobox/Motion/researchflow/p1_event_transfer_20260516/outputs/run_20260517_l40_multiscale`
  - local output: `eval/text_embedding_ext/run_20260517_l40_multiscale/`
  - 当前 active 用途：只保留 P1 full-vs-single rows 和 P1 compact rows；混入的旧 M0 rows 不作为当前 active evidence。
  - refetched artifact: `artifacts/remoteL40/p1_event_transfer_l40_multiscale_refetch_20260518/run_20260517_l40_multiscale/`
  - encoders: `distilbert_base_uncased_mean`、`t5_base_mean`、`t5_large_mean`、`flan_t5_base_mean`、`qwen3_32b_mean`
  - row_counts at original run: `p1_all=150`、`m0_all=360`、`p1_compact=145`、`m0_compact=20`
- DistilBERT 增量 run 已完成：
  - model_id: `distilbert-base-uncased`
  - remote log: `/sata/public/ripemangobox/Motion/logs/p1_distilbert_text_embedding_20260518_rerun.log`
  - local log: `logs/p1_distilbert_text_embedding_20260518_rerun.log`
  - backup before incremental run: `/sata/public/ripemangobox/Motion/researchflow/p1_event_transfer_20260516/outputs/run_20260517_l40_multiscale_pre_distilbert_20260518`
  - output: `eval/text_embedding_ext/run_20260517_l40_multiscale/encoders/distilbert_base_uncased_mean/`
- 有效性复查：三个 T5 encoder 全部 finite；Qwen3-32B mean pooling 只有 `11/30` P1 pairs 为 finite。因此 Qwen 当前 run 只作为诊断/失败信号，不作为主排序证据。
- DistilBERT 有效性复查：P1 pairs 为 `30/30` finite。

## 后续 Gate

1. 按 `eval/text_embedding_ext/run_20260517_l40_multiscale/aggregate/` 和 `results/compact_tables/` 复查 P1 跨 encoder 趋势，主结论优先使用 finite coverage 完整的 T5/DistilBERT 系列。
2. 若继续使用 Qwen，先修复非有限 hidden state，并补测 `last_token_final_hidden` 与中后层 layer sweep。
3. 如需图形化，再基于 aggregate TSV 生成 `vis/summary/text_embedding_ext/`。
4. 后续结论仍保持 `role=diagnostic`，不能替代 motion-side 或 human judgement。

## 元数据

- date: `2026-05-17`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `remoteL40_setup_probe`
- protocol: `SSH/MCP setup and text encoder weight staging preflight`
- data_source: `~/.ssh/config; /home/ripemangobox/mcp/remote4090; /home/ripemangobox/mcp/remoteL40; L40 ssh probes; artifacts/remoteL40/p1_event_transfer_l40_multiscale_refetch_20260518`
- condition_pair: `not_applicable`
- n/evaluable: `1/1 MCP direct status smoke passed; 3/3 T5 weight dirs staged; 1/1 Qwen32B download completed; 5/5 text encoders evaluated`
- coverage: L40 host connectivity, GPU visibility, MCP local code registration, T5/Qwen/DistilBERT weight staging, P1 text-side diagnostic run
- role: `diagnostic`
- used_for: `observation`
- limitations: Text-side pooled embedding only；不是 generator propagation、motion correctness 或 final evaluator 证据；Qwen3-32B mean pooling 当前 finite coverage 不足，不能作为主排序证据；DistilBERT 不是专用 sentence embedding 模型，只作为轻量 encoder 诊断补充。
