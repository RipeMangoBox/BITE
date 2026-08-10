---
title: "StoryMotion 配置驱动实验运行层"
hypothesis: "将主机适配、运行路径、GPU 映射和阶段命令收敛为严格配置，可以减少版本脚本复制，同时保持模型与评测语义的代码所有权。"
status: active
archived: 2026-08-03
source_papers: []
tags:
  - StoryMotion
  - engineering/runtime
  - experiment-contract
created: 2026-07-29T23:10:22+08:00
updated: 2026-07-29T23:10:22+08:00
---

# StoryMotion 配置驱动实验运行层

> [!abstract] 结论
> StoryMotion 不应继续为每台主机和每个实验阶段复制 launch、path、GPU、contract、preflight、resume 与 evaluate 适配代码。公共运行层负责这些机械边界；版本目录只保留真正不同的 model、data、objective 和 evaluator adapter。历史脚本仍是旧 run 的代码 provenance，不批量改写或删除。

## 目标与非目标

本页定义跨 4090、5090 与 3090 BITE 工作面的 durable runtime contract。它不拥有研究结论、运行进度或指标：当前主线仍由 [[ideas/StoryMotion/current|StoryMotion current]] 管理，正式数值仍由 [[ideas/StoryMotion-valid-metric-ledger|valid metric ledger]] 管理，指标语义仍由 [[ideas/StoryMotion-metric-computation-io|metric computation I/O]] 管理。

目标：

- 主机路径、Python 环境、PulpMotion 路径和 official model 路径只声明一次。
- 每个实验 family 只声明一次阶段入口；arm 仅保留 host、GPU、run ID 与真正变化的实验字段。
- 默认只展开命令；`--check` 验证主机、输入和运行时但不执行；`--execute` 才执行。
- 固定因果与表示边界继续由代码断言拥有，不搬入可变 run 配置。

非目标：

- 不用一个 mega-runner 合并不同模型、损失、数据流或 evaluator 语义。
- 不把 v10、v11、Unified-3 和外部 baseline 的算法差异降格为字符串开关。
- 不改写已关闭 run 所依赖的历史脚本，也不借通用化重排旧证据。

## 分层

```text
configs/storymotion_runtime/hosts.json
          + family plan JSON
                    |
                    v
storymotion/experiment_config.py
  严格校验 -> 路径展开 -> argv/env 物化
                    |
                    v
scripts/storymotion_configured_run.py
  dry-run / --check / --execute / immutable command record
                    |
                    v
experiment-owned adapter
  model / data / objective / evaluator semantics
                    |
                    v
experiment_contract.json + run-local logs/artifacts
```

## Canonical 文件

- `storymotion/experiment_config.py`：schema 校验、v11 fail-close 矩阵校验、路径与无 shell argv 展开。
- `scripts/storymotion_configured_run.py`：统一 CLI；执行前核对 hostname、入口、必需输入和精确 package 版本。
- `configs/storymotion_runtime/hosts.json`：4090、5090、`3090_bite` 的主机 profile。
- `configs/storymotion_runtime/v11_fixed_h_camera.json`：第一份迁移样例，拥有四臂映射和 phase argv 模板。
- `tests/test_storymotion_experiment_config.py`：矩阵、路径、checkpoint、禁用 parallel、目录逃逸与 host schema 回归。

4090 与 5090 的 StoryMotion 根均为 `/data/public/ripemangobox/Motion/StoryMotion`。`3090_bite` 的根为当前 BITE 工作面 `linkedCodebases/StoryMotion`；在精确环境和授权资产未完成审计前，它保持 `execution_ready: false`，允许 render 命令但拒绝执行。

## 配置所有权

| 配置层 | 可以拥有 | 禁止拥有 |
| --- | --- | --- |
| host profile | StoryMotion root、Python、runs root、Pulp/data/model 路径、hostname | loss、batch、表示维度、因果设置 |
| family plan | arm 到 host/GPU/run ID 的映射、phase entrypoint 与 argv、运行时 package 版本 | 训练实现、decoder 语义、隐式默认 checkpoint |
| experiment contract | mutable checkpoint/cache/stat hash、split、sample ID、seed、batch、sampler | 手工重复固定表示设置 |
| code invariant | 非因果、latent order、固定 feature contract、v11 禁止 joint parallel | 主机路径与一次性 run ID |

## v11 第一份等价迁移

v11 plan 固定拒绝以下漂移：

- `is_causal` 不为 `false`；
- generation modes 不是 completion 加 sequential；
- `joint_parallel` 不为 `false`；
- optimizer steps 不是 30K；
- 四臂集合不是 LAT/GEO 乘 GT-only/GT64+teacher64；
- resume/evaluate 未提供 step；
- entrypoint 为绝对路径或包含 `..`。

这些检查只保护运行矩阵，不重新声明 Stage1 的固定表示。Stage1 checkpoint、owning decoder、cache 与 stats 的精确 SHA 仍由各 run 的 `experiment_contract.json` 和现有 dependency verifier 核对。

## 使用

默认 dry-run：

```bash
python scripts/storymotion_configured_run.py \
  --plan configs/storymotion_runtime/v11_fixed_h_camera.json \
  --arm C1-GEO \
  --phase resume \
  --step 5000
```

只做执行前检查：

```bash
python scripts/storymotion_configured_run.py \
  --plan configs/storymotion_runtime/v11_fixed_h_camera.json \
  --arm C0-LAT \
  --phase evaluate \
  --step 10000 \
  --check
```

执行并保留命令记录：

```bash
python scripts/storymotion_configured_run.py \
  --plan configs/storymotion_runtime/v11_fixed_h_camera.json \
  --arm C0-LAT \
  --phase evaluate \
  --step 10000 \
  --record runs/train/stage2/RUN_ID/commands/evaluate_010000.json \
  --execute
```

`--record` 使用 create-only 写入；已有文件会失败，不覆盖历史命令。runner 不通过 shell 拼接训练参数，GPU 由 `CUDA_VISIBLE_DEVICES` 环境字段物化，进程内设备固定为 `cuda:0`。

## 迁移策略

### 已完成：公共 orchestration 边界

- 收敛三主机 profile。
- 收敛 v11 preflight/train/resume/evaluate 命令模板。
- 将 PyTorch3D 等 evaluator 依赖纳入执行前精确版本检查。
- 为 v11 formal sequential 与四臂矩阵增加配置层 fail-close。

### 下一步：按 family 逐个迁移

1. 活跃 v11 run 关闭后，先迁移纯工具函数，如 JSON object 读取、atomic JSON、SHA 与 command record；迁移后必须生成新 code hash，不能让旧 contract 指向新实现。
2. 选择一个已关闭的 v10 或 protected-H 非正式诊断作等价回放，比较展开 argv、输入 hash 和输出 artifact schema。
3. 每次只迁移一个 family；通过回归后再处理下一个，不做全仓机械替换。
4. `make_*_contract.py` 中真正只是 parent contract patch 的变体可逐步改为 declarative patch schema；改变 causal question、task modes 或 evaluator 语义的变体继续保留独立 adapter。

### 保留的历史边界

现有版本化脚本可以被标记为 superseded，但不删除。它们与旧 checkpoint、contract 和 metric artifact 的 code hash 共同构成 provenance。通用层只面向新 run 或显式迁移后生成的新 contract。

## 验收

每个新增 family plan 至少通过：

- 所有 arm ID、host profile 与 GPU 映射唯一；
- dry-run argv 与旧入口逐 token 等价；
- `--check` 在目标主机验证 hostname、Python、输入文件和 package 版本；
- fixed invariant 的负例测试，包括 causal 与非法 generation mode；
- preflight 仍报告 optimizer 未启动；
- resume round-trip 保持 optimizer、EMA、RNG 和 dataloader cursor；
- evaluator artifact 继续声明具体 mode，v11 不出现 joint parallel。

> [!warning] 文档路由
> 本页不记录 step、ETA、screen 数值或正式指标。实时事件只写 run-local manifest/log；screen 只更新其 owning plan；正式审计后才更新 ledger、current 与 [[ideas/StoryMotion/version_family|version family]]。
