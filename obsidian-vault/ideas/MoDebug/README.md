---
created: 2026-05-01T15:05:48+08:00
updated: 2026-06-16T02:30:00+08:00
title: "MoDebug README"
status: active
hypothesis: "GDC-based semantic locking detection 已被 control pair 证伪。真正的有效机制是简单的 two-phase ω 调度（early strong CFG → late weak CFG），稳定性 18× 优于 SLAD Full。"
tags:
  - MoDebug
  - index
  - archive
  - v3
---

# MoDebug README

> [!abstract] 当前规则
> 根目录只保留索引、当前 v3 主线和历史归档入口。旧版 Trace 1/2/3、v1/v2 计划和旧实验都已移入 `archived/`；当前可执行进度以 2026-06-14 的 SLAD 接力为准。

## 当前主线

| 文件 | 角色 |
|------|------|
| [[2026-06-13_modebug_slad_v3]] | 当前主线；SLAD 设计、实验更新和 detector calibration。 |
| [[experiments/molingo/2026-06-14_slad_history]] | 最近两天的接力总结；formal suites、诊断边界和 MVP 设置。 |
| [[experiments/molingo/2026-06-14_slad_m0_prompt_swap_analysis]] | M0 formal suites 的结果分析；核心数值与边界说明。 |
| [[experiments/README]] | 实验索引；当前 baseline 入口与实验归档入口。 |

## 历史归档

| 文件 | 角色 |
|------|------|
| [[archived/v1/2026-06-02_modebug_context]] | v1-era session context，历史保留。 |
| [[archived/v2/README]] | v2 计划、机制框架和证据重估的归档入口。 |
| [[experiments/archived/v2/README]] | v2 实验记录的归档入口。 |

## 旧 Trace 命名

| Trace | 对应 Line | 状态 | 入口 |
|------|-----------|------|------|
| Trace 1 | Line 1 | archived | [[archived/v1/trace_1_ca_perturbation/README]] |
| Trace 2 | Line 2 | archived | [[archived/v1/trace_2_semantic_repr/README]] |
| Trace 3 | Line 3 | archived | [[archived/v1/trace_3_data_efficiency/README]] |

历史别名：

- 旧 Track B = Trace 1。
- 旧 Track C = Trace 2。
- 旧 Track A = Trace 3。

## 文件夹规则

```
MoDebug/
├── README.md
├── 2026-06-13_modebug_slad_v3.md
├── archived/
│   ├── v1/
│   └── v2/
└── experiments/
```

- `archived/` 只放历史计划、历史上下文和历史实验索引。
- `experiments/` 放当前实验索引、结果分析、命令和脚本。
- 真实实验原始数据、日志、模型输出、视频、指标文件不得写入 vault；统一写入 4090 `/data/public/ripemangobox/Motion/experiments/MoDebug/`。
- 未通过 DS 的 smoke/probe/path-validation 必须标记为 `engineering_validation_only`，不能填入正式指标表。

## 4090 快速参考

| 组件 | 路径 |
|------|------|
| MotionCLR | `/data/public/ripemangobox/Motion/MotionCLR` |
| MoLingo | `/data/public/ripemangobox/Motion/MoLingo` |
| HumanML3D | `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D` |
| MoDebug 实验根 | `/data/public/ripemangobox/Motion/experiments/MoDebug` |
| MotionCLR release probe | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/setup/20260602_motionclr_release_float32_pipeline_probe` |
| MotionCLR generate CLI probe | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/setup/20260602_motionclr_release_generate_no_fp16_cli_probe_v2` |
| Conda env | `event-t2m` |

## 当前数据状态

当前可引用的结果已切到 SLAD v3。历史 MotionCLR / v1 / v2 记录都保留在归档里。

**已完成的三轮实验（2026-06-13 → 2026-06-15）：**

| 轮次 | 实验 | 规模 | 核心结论 |
|---|---|---|---|
| 1 | M0 prompt-swap | 1 seed × 8 pairs | 早期锁定现象确认 (12/14 ≤ step 8) |
| 2 | GDC calibration | 5 seeds × 8 pairs | Attribute 通过 (Pearson 0.81), action 未通过 (0.61) |
| 3 | SLAD vs baselines | 1-2 seeds × 4 modes | **SLAD 一致提前 locking (attr -0.25, action -0.37)**, C2FG 不稳定, ANT ≈ CFG |
| 4 | **SLAD ablation** ★ | 2 seeds × 5 conditions | **三组件（GDC/direction decoupling/projection）贡献均为零或负面**；真实机制 = two-phase ω |

**核心发现：**
- **Ablation 路线重定**：SLAD 的全部收益来自两段式 guidance（early strong → late weak），不需要 GDC detector / direction decoupling / semantic projection
- Paper 叙事简化为：简单 two-phase guidance > 所有复杂设计
- **Fixed step=25 与 GDC 自适应检测完全等效**（degrad 0.00）

**2026-06-16 已完成：**

| 轮次 | 实验 | 规模 | 核心结论 |
|---|---|---|---|
| 5 | **简化 SLAD 实现** | code change | `cfg_schedule=slad_simple`，纯 two-phase ω，无 GDC/decouple/project |
| 6 | **Multi-seed 验证** | 3 seeds × 3 conditions × 2 dims | 简化版方差 18× 低于 SLAD Full；control pair 暴露 GDC 致命缺陷 |

**🚨 2026-06-16 最重要的发现：**
- **Control pair（walks↔walks）在 SLAD Full 下 k50=3.94**——GDC 将噪声方向误识别为 semantic locking
- GDC 测量的是方向一致性，不是语义变化——这是根本性的 mismeaurement
- **GDC-based detection 已被 control pair 正式证伪**

**下一步：**
1. ⏳ **调优 split/ω_post** — 当前 split=0.5, ω_post=1.5 可能次优
2. ⏳ **MDM 跨模型** — 简化版 SLAD 只需修改 denoise loop 的 ω 调度
3. ⏳ **Evaluator 连接** — FID/R-Precision

详细数据、表格和证据边界见 [[2026-06-13_modebug_slad_v3]] §11-12 和 [[experiments/molingo/2026-06-14_slad_history]]。
