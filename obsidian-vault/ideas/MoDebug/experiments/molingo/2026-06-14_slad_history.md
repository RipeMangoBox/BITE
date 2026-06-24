---
created: 2026-06-14T13:15:12+08:00
updated: 2026-06-16T02:30:00+08:00
title: "MoDebug SLAD History / Handoff (2026-06-13 to 2026-06-16)"
status: simplified_multi_seed_completed
tags:
  - MoDebug
  - MoLingo
  - SLAD
  - history
  - handoff
  - status/calibration_completed
source:
  - "obsidian-vault/ideas/MoDebug/archived/v2/2026-06-13_modebug_research_framework_v2.md"
  - "obsidian-vault/ideas/MoDebug/2026-06-13_modebug_slad_v3.md"
  - "obsidian-vault/ideas/MoDebug/experiments/molingo/scripts/modebug_slad.py"
  - "obsidian-vault/ideas/MoDebug/experiments/molingo/commands/run_slad_core_gpu0_action_control_20260614.sh"
  - "obsidian-vault/ideas/MoDebug/experiments/molingo/commands/run_slad_core_gpu1_attribute_direction_20260614.sh"
  - "obsidian-vault/ideas/MoDebug/experiments/molingo/2026-06-14_slad_m0_prompt_swap_analysis.md"
  - "/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/slad/slad_core_calibration_*_20260614_core_seed5_official_gpu*"
---

# MoDebug SLAD History / Handoff

> [!abstract] 接力摘要
> 2026-06-13 单 seed M0 完成 → 2026-06-14~2026-06-15 双卡 5-seed calibration 完成。GDC stability_score detector 在 attribute 维度通过校准门槛（Pearson 0.81），action 维度未通过（0.61）。下一步：attribute 维度启动 SLAD vs baselines。

## 关键变化（截至 2026-06-15）

### 路线重定

- 2026-06-13 的 `v2` / `v3` 文档把 MoDebug 主线收敛到 semantic locking-aware decoupled guidance，layer specialization 退回参考位。
- 旧的 layer probe 叙事没有被删除，但已经降级为背景约束，不再是当前接力目标。

### 实现落地

- `modebug_slad.py` 合并了 `m0_swap` 和 `gdc_probe`，并保留 CFG equivalence 校验、outer swap sweep、inner trace 记录。
- GPU0 / GPU1 的 core calibration wrappers 已部署，双卡并行 pipeline：M0 swap → GDC probe → CPU 相关性分析。

### 结果

**Phase 1**（6/13 单 seed）：两个 formal suites 完成，`102` rows、`0` failures。CFG equivalence 验证通过。
**Phase 2**（6/14→6/15 calibration）：5 seeds × 8 prompt pairs × 2 directions，双卡 ~90 分钟。GDC detector 部分通过。
**Phase 3**（6/15 SLAD vs baselines）：4 种 guidance 模式对比 + action 诊断。SLAD 一致提前 locking，C2FG 极不稳定，ANT ≈ CFG。
**Phase 4**（6/15 ablation）：5 条件 × 2 维度 ablation。**核心结论：SLAD 机制是简单的两段式 guidance，GDC detector、direction decoupling、semantic projection 均可去掉。**
详细结果见 [[ideas/MoDebug/2026-06-13_modebug_slad_v3#11. 2026-06-15 实验更新：Multi-Seed Calibration 完成|v3 §11]]。

### Calibration 核心数字

| 维度 | k50 mean | k50 ≤ step 8 | Best GDC Pearson | 通过 |
|------|---------|-------------|-----------------|------|
| action/control (GPU0) | 5.98 ± 2.67 | 77% | 0.613 (stability, θ=0.90) | 否 |
| attribute/direction (GPU1) | 5.29 ± 2.77 | 92% | **0.813** (stability, θ=0.95) | **是** |

### 方向不对称（跨 seed 一致）

- kicks↔punches ratio **2.54**: a→b 始终远晚于 b→a
- jumps↔height ratio **2.12**: 同向不对称
- walks↔forward/backward ratio **0.49**: 反向不对称
- speed pairs 和 turn pairs 几乎对称（ratio ~1.0）

## 当前边界

- M0 endpoint-distance 证据在 5 seeds 下稳定，SLAD vs baselines 在 1-2 seeds pilot 下正向，但仍不是 official evaluator。
- **GDC 校准质量 ≠ SLAD 效果**：decoupled guidance 的方向分解可能独立于精确 locking 检测起作用。
- C2FG 固定指数衰减在 motion 上极不稳定，ANT 等价于 CFG baseline。
- 方向不对称仍然显著，`a_to_b` 与 `b_to_a` 必须分开报告。

## 下一步（按优先级）

Ablation 已完成，核心结论出乎意料：SLAD 不需要复杂机制。下一步：

1. **简化 SLAD 为 two-phase guidance**：去掉 GDC detector 和 decoupling，只用 early strong CFG + late weak CFG。与 ANT fixed two-phase 的核心区别是切换点（~step 25/50 vs 60%/40%）。
2. **Multi-seed 确认简化版 SLAD**：3+ seeds 估计方差。
3. **MDM 跨模型**：简化版 SLAD 只需修改 denoise loop 的 ω 调度，比原版更容易跨模型。
4. **Evaluator 连接**：FID/R-Precision。

---

## 2026-06-15 接力：简化版 SLAD 实现与 Multi-Seed 验证

> 来自 HANDOFF_PROMPT_20260615.md 的接力任务。

### 代码修改

**`modebug_slad.py` 新增 `cfg_schedule=slad_simple`：**
- 在 `cfg_for_outer_step()` 中添加 `slad_simple` 分支
- 新参数：`--slad_split`（timestep fraction，默认 0.5 = step ~25/50）、`--slad_omega_post`（post-split ω，默认 1.5）
- 核心逻辑：`timestep < slad_split → cfg (5.5)` else `slad_omega_post (1.5)`
- 使用 `guidance_mode=cfg`（无需 SLAD 内部 GDC/direction 逻辑）
- 在 manifest settings 中记录 `slad_split` 和 `slad_omega_post`

**Shell 脚本：** 新建 `run_slad_simple_multiseed_20260615.sh`，3 seeds × 3 条件（CFG baseline / Simplified SLAD / SLAD full）。

### Multi-Seed 验证结果（2026-06-16 完成）

- **完成时间**：2026-06-16 02:20 CST（耗时 ~170 min）
- **状态**：6/6 条件完成，0 failures，CFG equivalence 全通过（max_abs=0.0）

**Per-pair k50 完整结果：**

**Action Control:**
| Pair | CFG | Simplified SLAD (Δ) | SLAD Full (Δ) |
|------|-----|-------------------|---------------|
| walks↔walks (ctrl) | 0.00 | 0.00 (0.00) | **3.94 (+3.94)** 🚨 |
| walks↔runs | 5.51 | 5.39 (−0.13) | 4.83 (−0.68) |
| sits↔stands | 4.92 | 4.91 (0.00) | 5.03 (+0.12) |
| kicks↔punches | 7.23 | 7.10 (−0.12) | 6.26 (−0.97) |

**Attribute Direction:**
| Pair | CFG | Simplified SLAD (Δ) | SLAD Full (Δ) |
|------|-----|-------------------|---------------|
| slowly↔quickly | 4.11 | 4.11 (0.00) | 3.88 (−0.23) |
| jumps high↔low | 8.96 | 8.52 (−0.44) | **7.45 (−1.51)** |
| forward↔backward | 5.56 | 5.29 (−0.27) | **4.44 (−1.12)** |
| turns left↔right | 4.88 | 4.88 (0.00) | 5.13 (+0.26) |

**🚨 关键发现：Control pair 暴露 GDC 致命缺陷**

Control pair（walks↔walks，相同 prompt）在 CFG 和 Simplified SLAD 下正确给出 k50=0.00（无 swap 效应）。但 SLAD Full 将其推到 k50=3.94——GDC 检测器错误地将去噪噪声识别为 "semantic locking"，篡改了 guidance。**GDC 测量的是方向一致性，不是语义变化——这是根本性的 mismeaurement。**

**核心结论：**
- GDC-based 检测已被 control pair 证伪——方向一致性 ≠ 语义锁定
- 简化版 SLAD 方差远低于 SLAD full（action 18×, attribute 3×），无副作用
- SLAD Full 的 "优势" 主要来自 outlier suppression（seed=2026 jumps k50 19.0→9.5），不是系统性改善
- Paper 叙事定稿：简单两段式 ω 调度 > 复杂自适应检测
