---
title: MoDebug Session Context
created: 2026-06-02T00:00:00+08:00
updated: 2026-06-14T00:00:00+08:00
status: archived
hypothesis: "Historical session context for the v1/v2 phase; the live handoff is now in the SLAD history note."
tags:
  - MoDebug
  - context
  - handoff
  - archive
  - v1
  - status/archived
---

# MoDebug Session Context

> [!abstract] 已归档
> 这份上下文保留 v1/v2 时代的接力信息。当前可执行进度请看 [[experiments/molingo/2026-06-14_slad_history]]，当前主线请看 [[2026-06-13_modebug_slad_v3]]。

## 2026-06-07 当前进展

> [!note] 当前定位
> 本轮 4 个 baseline 的 eval 不是为了做 leaderboard，也不要求 4 个 baseline 完全同构重构；它们服务于 MoDebug 对 text-motion alignment 与 motion generation quality 的学习机制诊断。目标是从逐层 SA/CA/CFG_SA/CFG_CA 干预结果中推断模型在不同层、不同 attention 路径、不同 CFG 分支上的职责差异，并进一步设计 post-train、pretrain、routing、regularization 或 evaluator-guided 的机制来提高对齐度和生成质量。

### Cross-baseline attention intervention 状态

| Baseline | 当前状态 | 关键用途 |
|---|---|---|
| MotionCLR | 20260605 formal outputs 完成；baseline、SA、CA、CFG_SA、CFG_CA 均有 full evaluator metrics | 主要机制信号源；CFG_CA 12-15 层强退化，提示 CFG cross-attention 边界/中后层可能是 alignment-quality 冲突区。 |
| MotionGPT | baseline、SA、CA 完成；CFG_SA/CFG_CA fail-fast 为 unsupported | 对照组；SA/CA 干预接近 baseline，提示该架构下层职责可能更冗余或 intervention 不足以暴露机制。 |
| MoLingo | baseline、SA、CA、CFG_SA、CFG_CA 完成；TMR 指标面板 | 第二个完整 CFG 对照；FID_TMR 对部分层敏感，但 Top1/Top2/Top3 相对稳定，提示 quality distribution 与 text retrieval alignment 可分离。 |
| MotionStreamer | encode-cache 版本正在运行；只应补 SA/CFG_SA，CA/CFG_CA 因架构阻断 | causal self-attention 架构对照；完成后用于检查无 CA 模块模型是否仍有 stage/block-level 敏感模式。 |

结构化结果和图位于本地整理面：`linkedCodebases/MoDebug/attention_intervention/`。其中 `results/summary.md` 是综合报告；`visualization/data/source_metrics_20260605.json` 是从远端 formal roots 导出的审计源数据；`visualization/data/family_summary.csv` 与 `layer_metrics.csv` 已补齐 R-Precision Top1/Top2/Top3。

### 当前可引用观察

- MotionCLR：CFG_CA family 的均值显著退化，FID mean `0.7025`、Top1/Top2/Top3 mean `0.3793/0.5619/0.6662`、Matching mean `4.0675`；其中 12-15 层是主要异常区。SA、CA、CFG_SA 大多数层接近 baseline，但 late SA/CFG_SA 有 FID spike。
- MotionGPT：SA/CA 相对 baseline 基本稳定，甚至 SA 的 Top1/Top2/Top3 mean 略高于 baseline；这不能直接说明“没有分工”，更可能说明该 intervention 对该架构的可观测性不足或层间冗余更强。
- MoLingo：CFG_SA/CFG_CA 的 FID_TMR mean 上升，但 Top1/Top2/Top3 mean 只小幅变化；这提示文本检索对齐和 motion distribution quality 可能由不同机制支撑。
- 三个已完成 baseline 的原始 `metrics_summary.json` 均含 Top1/Top2/Top3；当前 Top1/Top2 图和 CSV 不是由 Top3 反推。

### 工具链进展

- `research-brainstorm-from-kb` 已修正为当前 index 契约：`index.jsonl` + `by_topic/`、`by_method/`、`by_dataset/`、`by_venue_year/`；不再使用旧 `by_venue/`、`by_year/`。
- `papers-query-knowledge-base` 和 `research-workflow` 的 index 描述已同步修正。
- 已重建 `obsidian-vault/index`：`index.jsonl` 1628 条，`by_venue_year/` 已生成，旧 `by_venue/`、`by_year/` 不存在。

### DS max 质询后的机制判断

> [!important] 证据边界
> DS max 复核后的保守结论是：当前三 baseline 支持“模型对 layer/stage/module intervention 的敏感性不同”，但还不能写成“每层都有独立语义分工”。更强的 paper 叙事应从“可证伪的 functional specialization / alignment-quality coupling”出发，而不是从逐层曲线直接命名语义角色。

当前可支撑的性质：

- MotionCLR 的 CFG_CA 退化是最强机制信号：单独 CA 和 CFG_SA 影响较小，而 CFG_CA 在 12-15 层显著破坏 FID、R-Precision 和 Matching，说明中后层 CFG cross-attention 或 cond/uncond boundary 可能是 alignment-quality 耦合区。
- MoLingo 的 CFG 干预主要伤害 FID_TMR，而 R-Precision 基本稳定，说明 retrieval alignment 与 motion distribution quality 至少在指标层面可分离；这需要继续用属性级 quality probe 验证，不能直接等同于表示完全解耦。
- MotionGPT SA/CA 接近 baseline 只能说明当前 intervention 没有暴露强敏感区；可能是架构冗余、干预可观测性不足、CFG 路径缺失或对齐分散在表示空间中，不能写成“无分工”。
- MotionStreamer 仍 pending；它的作用是验证无 CA 模块的 causal self-attention 架构是否仍出现 stage-level 敏感性，不能提前纳入结论。

DS max 建议把下一步收敛为三个最小处理包：

1. MotionCLR 12-15 层做单层级 activation patching / swap-restore，区分“某一核心层”与“block-level 耦合区”。
2. 对 MoLingo 增加帧段/属性级质量分析，检查 FID_TMR 退化来自 transition、contact、smoothness、diversity 还是全局语义偏移。
3. 对 MotionGPT 改用 representation probing 或更强 stress test，避免因为 SA/CA 指标稳定就过早否定机制差异。

机制设计因此应围绕两条主线：一条是 post-train / CFG-specific regularization 修复 MotionCLR 式 cond/uncond boundary；另一条是 attribute evaluator / reward / preference 把逐层干预失败样本转成训练信号，分别服务于 text-motion alignment 与 motion quality。

研究讨论初稿见 [[../2026-06-07_motion-layerwise-specialization]]。后续如果 MotionStreamer 正式指标完成，需要把无 CA 架构的 SA/CFG_SA 结果补入同一证据表，再决定是否把叙事从 MotionCLR-specific CFG pathology 扩展到 cross-architecture stage specialization。

## 2026-06-14 SLAD update

- MoLingo SLAD M0 formal suites 已完成，分析见 [[experiments/molingo/2026-06-14_slad_m0_prompt_swap_analysis]]，接力记录见 [[experiments/molingo/2026-06-14_slad_history]]。
- 当前结论仍是 trajectory-level diagnostic evidence，不是 official evaluator 或 human eval。
- 下一步仍是补至少 3 个 seeds，并加 inner-ODE GDC trace 做 detector 校准。

## 当前命名

| Trace | 对应 Line | 旧称 | 状态 |
|------|-----------|------|------|
| Trace 1 | Line 1 | Track B | CA 层扰动诊断，active |
| Trace 2 | Line 2 | Track C | 语义表征，demoted |
| Trace 3 | Line 3 | Track A | 数据效率训练侧，active |

## 4090 状态

| 项目 | 状态 |
|------|------|
| GPU | 2× RTX 4090；2026-06-07T23:12+08:00 GPU0 跑 MotionStreamer encode-cache SA，GPU1 跑 MotionStreamer encode-cache CFG_SA |
| MotionCLR repo | `/data/public/ripemangobox/Motion/MotionCLR` |
| MotionCLR HEAD | `a6f44a791940682fe335c82f1b436bae05a1cebb` |
| MotionCLR dirty tracked files | `scripts/generate.py`、`utils/plot_script.py`，均为已知 setup fixes |
| HumanML3D | 已配置，真实数据路径可用 |
| Conda env | `event-t2m` |
| 当前 tmux | `ms_encodecache_sa_gpu0_20260607`、`ms_encodecache_cfgsa_gpu1_20260607` |
| Serial supervisor | 2026-06-03 旧接力 supervisor；保留为历史记录，不是当前 MotionStreamer 运行入口 |

## 已降级记录

以下远端 run 已写入 `NONFORMAL_NOTICE.txt`，并在 manifest/runtime status 标注为 `engineering_validation_only`：

| Trace | 远端路径 | 不可用于正式结论的原因 |
|------|----------|------------------------|
| setup | `motionclr/setup/20260602_motionclr_release_generate_no_fp16_cli_probe_v2/` | 2-step generate CLI 验证，不是质量指标。 |
| Trace 1 | `motionclr/track_b_ca_perturbation/20260602_gpu1_track_b_ca_cfg_sweep_mvp/` | empty `cond_indices` 不是 CA-only 扰动。 |
| Trace 3 | `motionclr/track_a_disploss/20260602_gpu0_track_a_minimal_real_ablation/` | OOM/停止/不完整 checkpoint，只是训练路径验证。 |

## DS 状态

历史 DS session `eda0968dad94` 的 `BLOCKED` 已被 2026-06-03 新复核取代。新 DS 结论先批准 formal candidate 启动；Trace 1 结果分析随后经 DS 复核为 `APPROVED_WITH_CAVEATS`。记录见 [[experiments/archived/v2/motionclr/2026-06-02_ds_formal_experiment_gate]] 和 [[experiments/motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。

本轮已完成双卡 bounded real-data validation，记录见 [[experiments/archived/v2/motionclr/2026-06-02_dual_trace_bounded_validation_status]]：

- GPU1 / Trace 1：真实 MotionCLR release checkpoint + 真实 prompt，验证 CA output scaling hook 的 no-op 和 positive control。
- GPU0 / Trace 3：真实 HumanML3D train split + MotionCLR 训练路径，验证精确步数停止和真实 batch update，不报告正式训练收益。

> [!warning] 接力更正
> 上述 bounded validation 不是正式实验。前一轮把它汇报为“双 Trace 测试完成”过度简化了边界；用户已指出正式 Line 1 至少需要 18 层逐层扰动和 CFG 条件半边同层 uncond latent/hidden state 替换，总计至少 36 组，Line 3 必须是真训练。2026-06-03T15:25+08:00 起，正式候选实验已启动，但仍未形成 paper-level 指标。

## 2026-06-03 旧正式候选运行记录

| Trace             | tmux                                            | GPU  | 远端路径                                                                                                                                               | 当前状态                                                                                                                                                 |
| ----------------- | ----------------------------------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Trace 1           | `modebug_trace1_formal_20260603`                | GPU1 | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_formal_layer_sweep_ds_review_20260603_gpu1/`              | 已完成；36 个逐层 layer group 完成，controls passed，分析和折线图见 [[experiments/motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。 |
| MotionCLR Trace 3 | `modebug_trace3_train_formal_20260603`          | GPU0 | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0/`                    | 历史训练侧接力记录；本轮 cross-baseline eval 结论不依赖该项。 |
| MoLingo Trace 1   | `modebug_molingo_trace1_formal_test64_20260603` | GPU1 | `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_test64_ds_review_20260603_gpu1/` | 历史 test64 formal diagnostic 记录；当前已在 cross-baseline summary 中整理为 MoLingo 完成项。 |

## 2026-06-03 Serial Supervisor 归档

- local script: `obsidian-vault/ideas/MoDebug/experiments/commands/modebug_serial_supervisor_4090.sh`。
- remote script: `/data/public/ripemangobox/Motion/experiments/MoDebug/commands/modebug_serial_supervisor_4090.sh`。
- tmux: `modebug_serial_supervisor_20260603`。
- log: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug_serial_supervisor_20260603.log`。
- behavior: 先等待当前 MoLingo test64 formal 的 `manifest.json`，校验 `failures=[]` 与 `num_prompts>=64`；再等待 MotionCLR Trace3 四个 training manifest；最后串行运行 Trace3 official eval 并写 `eval_done.marker`。
- first status: 2026-06-03T18:16+08:00 已识别 MoLingo formal 正在 tmux 运行，并进入 300s 轮询等待，没有重复启动 MoLingo run。

## MoLingo 接力注意

- v4 dev validation output: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/dev_validation/molingo_trace1_formal_layer_sweep_dev_20260603_gpu1_v4/`；`failures=[]`，两个 no-op allclose，两个 positive controls 非 allclose。
- formal prompt set: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/prompt_sets/molingo_trace1_formal_test64_20260603.txt`，从 272D HumanML3D test split 固定抽取 64 条 caption。
- formal log: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_trace1_formal_test64_20260603_gpu1.log`。
- aborted run: `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/formal_candidates/molingo_trace1_formal_layer_sweep_ds_review_20260603_gpu1/` 只使用 MoLingo demo `assets/example.txt` 的 10 条 prompt，已停止，不纳入结论。
- 脚本已加入 `--prompt_count_min`，防止 formal prompt 数不足时静默继续。

## 下一步

1. 等 MotionStreamer encode-cache SA/CFG_SA 完成后，补入 `linkedCodebases/MoDebug/attention_intervention/` 的结构化数据、图和综合报告。
2. 对 MotionCLR CFG_CA 12-15 层做单层 activation patching / swap-restore / CFG scale sweep，确认是单层核心点还是 block-level 耦合区。
3. 对 MoLingo 的 CFG 退化补属性级 quality 分析，优先 contact、smoothness、transition、diversity。
4. 对 MotionGPT 做 representation probing 或 stronger stress test，避免把当前 SA/CA 稳定误读成“无机制”。
