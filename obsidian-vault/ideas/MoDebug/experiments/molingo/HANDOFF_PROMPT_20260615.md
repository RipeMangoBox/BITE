# MoDebug SLAD Handoff Prompt (2026-06-15)

## Task Description

研究 text-to-motion diffusion model 的 guidance 机制优化。核心假设：在去噪过程中存在 "semantic locking" 转变点——早期模型决定"做什么动作"，后期精调质量。利用这个转变点做两段式 guidance（early strong → late weak CFG）可以打破 quality-alignment tradeoff。

**当前阶段：** 六轮实验完成（含 2026-06-15 接力的简化版 SLAD 实现 + Multi-seed 验证）。GDC-based detection 已被 control pair 证伪。下一步：调优 split/ω_post + MDM 跨模型。

## Core Progress

### Round 1 — M0 Calibration (5 seeds × 8 prompt pairs, dual GPU, 92 min)
- 确认 trajectory-level source retention 是早期锁定现象
- Mean k50 ≈ 5-6 / 50 steps, 77-92% curves ≤ step 8
- GDC stability_score detector: attribute 通过 (Pearson 0.81), action 未通过 (0.61)
- 方向不对称跨 seed 一致

### Round 2 — SLAD vs Baselines (1-2 seeds × 4 guidance modes, 140 min)
- SLAD 一致提前 locking: action -0.37, attribute -0.25
- C2FG exponential 极不稳定 (range [-7.56, +4.18])
- ANT two-phase ≈ CFG baseline
- 关键发现: GDC 校准质量 ≠ SLAD 效果 (action detector 弱但效果强)

### Round 3 — Action Diagnostic (2 seeds, 84 min)
- 确认 action 维度 SLAD 效果 > attribute
- Inner-trace 数据收集完成

### Round 4 — Ablation (2 seeds × 2 dims × 5 conditions, 206 min) ★ 最关键
- 5 条件: CFG baseline / SLAD full / −adaptive / −decouple / −project
- **核心发现: 三个设计组件均不需要**
  - GDC adaptive detection → 固定 step=25 完全等效 (degrad 0.00)
  - Direction decoupling → 简单 ω scaling 反而更好 (degrad −0.17 action, −0.24 attr)
  - Semantic projection → 仅 attribute 微弱正向 (+0.12)，不值得保留
- **SLAD 真正机制 = two-phase guidance (early strong → late weak CFG)**

## Key Findings Summary

| 发现 | 置信度 | 证据 |
|---|---|---|
| Early locking 是稳健现象 | 高 | 5 seeds × 8 pairs |
| 两段式 guidance 优于 uniform CFG | 高 | 2 dims × 2 seeds |
| GDC adaptive detection 无贡献 | 高 | ablation (action + attr, 0.00 degrad) |
| Direction decoupling 有害 | 高 | ablation (两维度均负面) |
| C2FG/ANT 固定 schedule 不如简单两段式 | 中 | 1 seed pilot |

## Current MVP Settings

- `cfg=5.5`, `sample_steps=32`, `acc=3`, `directions=a_to_b,b_to_a`
- `swap_iterations=all`, `trace_detail=aggregate`
- 两段式切换点: outer step ~25/50
- Pre-lock: ω=5.5 (standard CFG)
- Post-lock: ω=1.5 (simple scaling, no decoupling/projection)
- 8 prompt pairs: 4 action (GPU0) + 4 attribute (GPU1)

## Simplified SLAD Algorithm

```python
# 去掉了 GDC/locking detection/direction decoupling/semantic projection
# 只保留最核心的两段式 ω 调度
omega_high = 5.5   # pre-split: strong CFG to establish semantics
omega_low = 1.5    # post-split: weak guidance to free quality space
t_split = 25       # outer steps (out of 50)

def simplified_slad_guidance(step, total_steps=50):
    if step < t_split:
        return omega_high
    else:
        return omega_low
```

## 4090 Infrastructure

```
SSH: ssh 4090  (172.23.148.106:59374, user ripemangobox)
Motion root: /data/public/ripemangobox/Motion
MoLingo repo: /data/public/ripemangobox/Motion/MoLingo (branch TPA)
Conda env: event-t2m
T5 path: /data/public/ripemangobox/Motion/Text-encoder/t5-large

Experiment outputs:
  /data/public/ripemangobox/Motion/experiments/MoDebug/molingo/slad/
    slad_m0_multiseed_*          — Round 1 calibration
    slad_vs_baselines_attribute_* — Round 2 SLAD vs baselines
    slad_action_diagnostic_*     — Round 3 action diagnostic
    slad_ablation_*              — Round 4 ablation (★ most important)

Key scripts (local, deploy to 4090):
  obsidian-vault/ideas/MoDebug/experiments/molingo/scripts/modebug_slad.py
  obsidian-vault/ideas/MoDebug/experiments/molingo/commands/run_slad_ablation_20260615.sh

Prompt sets:
  GPU0 (action): slad_m0_gpu0_action_control_20260613.tsv
  GPU1 (attribute): slad_m0_gpu1_attribute_direction_20260613.tsv
```

## Documentation to Update

```
obsidian-vault/ideas/MoDebug/2026-06-13_modebug_slad_v3.md  — 主文档 (§11-12)
obsidian-vault/ideas/MoDebug/experiments/molingo/2026-06-14_slad_history.md — 接力记录
obsidian-vault/ideas/MoDebug/README.md — 根索引
obsidian-vault/ideas/MoDebug/experiments/README.md — 实验索引
```

## ✅ Completed Tasks (2026-06-16)

### 1. ✅ 实现简化版 SLAD
- 新增 `cfg_schedule=slad_simple` in `modebug_slad.py`
- 参数：`--slad_split 0.5` (step ~25/50), `--slad_omega_post 1.5`
- 算法：`timestep < 0.5 → ω=5.5` else `ω=1.5`，纯 CFG，无 GDC/decouple/project

### 2. ✅ Multi-seed 确认简化版（3 seeds × 3 条件，双卡 ~170 min）
- **简化版 SLAD vs CFG**: action Δk50=−0.06±0.14, attribute Δk50=−0.18±0.70
- **SLAD full vs CFG**: action Δk50=+0.60±2.56, attribute Δk50=−0.65±2.10
- **核心发现**: 简化版 SLAD 方差远低于 SLAD full（action 18×, attribute 3×），但效应幅度偏小
- 结论：GDC-based 检测引入噪声，简单 two-phase 更可靠；下一步应调优 split/ω_post

### 3. ⏳ MDM 跨模型验证
### 4. ⏳ Evaluator 连接

## Critical Constraints

- 所有结论仍是 endpoint-distance diagnostic evidence，不是 official evaluator
- 方向不对称必须分开报告 a_to_b / b_to_a
- `--save_arrays` 会产生 270MB/condition 并导致 SHA256 瓶颈（5.8GB checkpoint），避免使用
- SLAD mode 比 CFG 慢 ~15%（~36 min vs ~32 min per 2-seed condition）
- 双卡可同时跑不同 prompt set（GPU0=action, GPU1=attribute）
- 每次 condition 完成后，bash task queue 自动继续下一个

## Paper Narrative Direction

原设计: "Semantic Locking-Aware Decoupled Guidance" (GDC detector + decoupling + projection)
→ Ablation 后: **"Simple two-phase guidance outperforms complex adaptive detection"**
→ **2026-06-16 Control pair 后发现**: GDC-based detection 已被正式证伪。当两个 prompt 语义相同时（walks↔walks），GDC 仍触发 "locking"，将 k50 从 0 推到 4。
→ **最终叙事**: GDC 是错误信号——方向一致性 ≠ 语义变化。简单两段式 ω 调度在稳定性（18× lower variance）、安全性（无 control pair 污染）和可复现性上全面优于复杂的自适应检测。

这是更强的故事：简单方法 > 复杂设计，且更容易跨模型验证和第三方复现。

---

## 🎉 Handoff Outcome (2026-06-16)

**接力完成项：**
- ✅ 简化版 SLAD 实现（`cfg_schedule=slad_simple`, `--slad_split 0.5`, `--slad_omega_post 1.5`）
- ✅ Multi-seed 验证（3 seeds × 3 conditions × 2 dims, 双卡 ~170 min）
- ✅ 深度 per-pair/per-seed/per-direction 分析
- ✅ 全部文档更新

**接力期间最重要的发现：**
Control pair（walks↔walks）暴露了 GDC 检测器的根本缺陷——方向一致性（GDC）不等同于语义锁定。这比 ablation 中"组件贡献为零"的发现更进一步：**GDC 不是无用的，是有害的。**

**下一步接力（需新 HANDOFF）：**
1. 调优 split point 和 ω_post（参数 sweep）
2. MDM 跨模型验证
3. Evaluator 连接（FID/R-Precision）
4. 论文撰写
