---
created: 2026-04-30T18:00
updated: 2026-05-01T16:05:43+08:00
title: "Paper A (EventProbe): 多事件运动生成的反事实诊断与评估方法论"
status: active
tags:
  - MoDebug
  - paper-plan
  - EventProbe
  - evaluation-methodology
  - diagnostic-benchmark
  - counterfactual-corruption
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
  - "[[2026-04-30_modebug-paper-b-perceptguide-plan]]"
---

# Paper A (EventProbe): 多事件运动生成的反事实诊断与评估方法论

## 1. 定位与核心主张

**类型**：Diagnostic benchmark + evaluation methodology + failure analysis paper。

**不是**：new generator paper；也不是 dataset paper。`HumanML3D-E` 已由 Event-T2M 提供，EventProbe 的贡献不是新数据，而是把已有 event decomposition 转化为难度可控、可复现、经 human calibration 的 event-level 诊断协议。

**核心主张**：

> 现有 full-level metrics（FID, R-Precision）会系统性漏掉多事件 motion generation 中的 omission、ordering violation 与 hard-negative semantic collapse。EventProbe 提出 human-calibrated event-counterfactual diagnostic protocol，在 `drop / hard-replace / shuffle` 上控制负例难度、按 event-count bucket 报告可靠性，并用 modern baseline failure atlas 揭示这些 event-level failure 与 full-level 指标弱相关或不相关。

**与最近邻工作的差异**：

- vs AToM (CVPR 2025)：AToM 用 GPT-4V reward 改善 event-level alignment；EventProbe 不训练生成器，而是测量自动 evaluator 在不同 corruption 难度、event bucket、baseline 输出上的可靠边界，并用 human calibration 作为 anchor。
- vs HumanML3D-E / Event-T2M (ICLR 2026)：Event-T2M 提供 event-level conditioning 与 HumanML3D-E；EventProbe 使用这套 event decomposition 做反事实诊断、hard-negative 控制、baseline failure atlas 和 scorer-selection leakage analysis。
- vs FineMotion (ICCV 2025)：FineMotion 贡献 fine-grained spatial-temporal annotation 与 benchmark；EventProbe 不扩数据标注，而是围绕多事件 prompt 的 omission / ordering failure 建立诊断协议与可靠性边界。
- vs ReAlign / EasyTune / Motion-R1 / MoRL：这些工作主要改进生成或对齐；EventProbe 的目标是提供可复查的 event-level failure measurement，用来压力测试这些现代方法是否真的改善多事件结构。

## 2. Contribution List

- C1: **Event-counterfactual diagnostic protocol**。提出 `drop / hard-replace / shuffle` 三类 text-side corruption、event-count bucket、difficulty-controlled negative construction，并区分 easy negative 与 hard negative，避免把简单替换造成的高 paired accuracy 误写成 evaluator 可靠。
- C2: **Human-calibrated event failure measurement**。构建 200-300 条 targeted human calibration set，覆盖 high-disagreement cases 与 high-event-count buckets，校准 TMR / ChronAccRet / optional MLLM/GPT-4V side signals，报告 agreement、confidence interval、per-bucket reliability 和自动 evaluator 失效边界。
- C3: **Modern baseline failure atlas**。在 historical anchors 与 modern baselines 上系统报告 omission、ordering、hard-negative collapse、event-count scaling failure，并验证这些 failure 与 FID/R-Precision 的关系；论文主 punchline 是 full-level evaluation 会系统性漏掉这些失败。

注：**Reward-metric fairness audit**。不把 held-out 写成贡献点；只把它作为实验卫生，并通过 scorer-selection leakage analysis 展示为什么 reward-side metric 不能作为 final improvement。

## 3. 必做实验

### A-P0: EventT2M retrain sanity + evaluator coverage fairness

Paper A 的 diagnostic benchmark 不能建立在未经复现的 pretrained checkpoint 上。A-EXP1 前必须先完成：

1. clean upstream EventT2M retrain，与官方 pretrained `hml3d.ckpt` 在同一 eval command 下比较。
2. ChronAccRet coverage audit：报告 HumanML3D-E test split、ChronAccRet evaluable subset、safe_drop_join rows 的 overlap、uncovered rows 和 event-count bucket 分布。
3. 若 retrain 与 pretrained 差异很大，A-EXP1 的 EventT2M baseline 必须分成 `EventT2M-pretrained` 与 `EventT2M-retrain` 两列，且论文不能把 pretrained 结果作为无条件可信根基。

### A-EXP1: 多 baseline 诊断

在 historical anchors 与 modern baselines 上跑 event-counterfactual diagnostic protocol（`drop / hard_replace / shuffle`），报告每个 baseline 的 corruption sensitivity、human-calibrated failure rate、event-count bucket 结果，以及与 full-level safety metrics 的相关性。

- 输入：各 baseline 的 checkpoint + HumanML3D-E test split；EventT2M 必须包含 pretrained 与 clean retrain sanity comparison
- 输出：per-baseline per-bucket diagnostic table；automatic side signals 与 human-calibrated failure rates 分开报告
- 预估：2-3 周（主要是跑 inference + TMR/ChronAccRet scoring）
- 与 Paper B 关系：**完全独立**，可与 B-EXP1 同时开始
- Baseline 覆盖说明：`MDM / MLD / MotionDiffuse` 只能作为 historical anchors；主表至少应包含 `Event-T2M`，并尽量加入 `ReAlign` 或 `EasyTune` 这类 reward/alignment baseline，以及 `Motion-R1 / MoRL / IRG-MotionLLM` 中至少一个 reasoning/LLM baseline（若能获得同 prompt 输出）。若 code/checkpoint/output 不可用，必须做 availability-limited comparison 表，而不是只写 qualitative 一句话。

### A-EXP2: Scorer-selection leakage 实验

证明当同一个 scorer/protocol 既用于 model selection / reward optimization 又用于 final evaluation 时，`heldout_final_evaluator` 上的 gain 会显著低于 `dev_scorer` 上的 gain。这里的 `held-out` 是公平性要求，不是 novelty claim。

- 设计：用 TMR 作为 dev scorer 选择负例策略（easy-replace vs hard-replace）和 reward 权重，然后分别用 TMR（dev）和 ChronAccRet + human eval（held-out）评估选出的最优配置
- 输出：dev-side gain vs held-out gain 的 gap table；如果 gap 显著（>5pp），则 scorer-selection leakage 成立
- 注意：仅比较已有 scorer rows 只能证明 scorer disagreement，不能证明 leakage。必须有一个被 TMR 优化/选择过的决策过程
- 预估：1-2 周（Paper A 独立版本用 negative strategy selection 作为 proxy；如果 Paper B 的 guidance 输出可用，再补真正 reward-optimization leakage）
- 与 Paper B 关系：**弱依赖**——最完整的 leakage 证据需要 B 的 guidance 输出；但可用 negative strategy selection 作为 Paper A 独立的 proxy 实验

### A-EXP3: Hard-negative replace 补充

已有 `hard_replace_lexical` 结果（`tmr_gt_pres_hard_replace_lexical_paired_acc = 0.6523`，`5plus = 0.5556`，`n=512`，role=diagnostic），需要补 TMR-embedding cosine hard-negative，验证 easy replacement 是否膨胀 paired accuracy。

- 输入：TMR embedding space + `aligned_replace_manifest.jsonl`
- 输出：`aligned_replace` vs `hard_replace_lexical` vs `hard_replace_tmr` 的 paired accuracy 与 human calibration 对比
- 预估：1 周
- 与 Paper B 关系：**完全独立**；结果可选择性反馈给 B-EXP1 的负例策略

### A-EXP4: Human eval 三角验证（核心证据，非附录）

TMR × ChronAccRet `safe_drop_join` agreement 只有 `73.32%`，`5plus = 63.75%`，说明自动 evaluator 本身不稳。human eval 必须作为 anchor 证据，不能降级为附录。

- 规模：200-300 条样本（覆盖 4 个 baseline × 多 event bucket），其中 high-disagreement 样本占 50%+
- 标注维度：omission（是否遗漏子动作）、ordering（子动作顺序是否正确）、severity（1-3 级）
- 输出：human-TMR agreement, human-ChronAccRet agreement, 三方 Fleiss kappa, per-bucket human accuracy 作为 evaluator 可靠性的 ground truth
- 预估：2-3 周（含标注设计 + 标注 + 分析）
- 前置：A-EXP1 + A-EXP5 完成后选样本
- 与 Paper B 关系：**完全独立**
- 论文定位：这是 Paper A 的核心 table 之一，不是 supplementary

### A-EXP5: Failure pattern 报告

从 A-EXP1 结果中提取跨 baseline 的系统性 failure pattern。

- 输出：failure atlas（如"5plus bucket 的 omission / order failure 系统恶化"、"hard-negative replace 暴露 semantic collapse"、"FID/R-Precision 与 human-calibrated event failure 弱相关"等）
- 预估：与 A-EXP1 同步
- 与 Paper B 关系：**完全独立**

## 4. 已完成可直接复用的资产

| 资产 | 来源 | Canonical metric / role |
|------|------|------|
| TMR omission dataset eval | `evaluator-status-summary.md` §4 | `tmr_gt_pres_full_vs_drop_paired_acc = 0.7044 (n=3799, role=side_signal)` |
| TMR default replace eval | `evaluator-status-summary.md` §2 | `tmr_gt_pres_full_vs_replace_paired_acc = 0.8363 (n=3799, role=side_signal)` |
| ChronAccRet ordering | `evaluator-status-summary.md` §2 | `chron_subset_ord_shuffle_car = 0.6474 (evaluable=2331/2333, role=formal_ordering_evidence)` |
| ChronAccRet omission | `evaluator-status-summary.md` §5 | `chron_subset_pres_full_vs_drop_paired_acc = 0.7300 (n=2333, role=cross_check)` |
| safe-drop consistency | `evaluator-status-summary.md` §7 | `tmr_chron_safe_drop_agreement = 73.32% (n=1608, coverage_tmr=42.33%, role=cross_check)` |
| aligned-replace consistency | `aligned_replace_consistency_summary.json` | `tmr_chron_aligned_replace_agreement = 81.65% (n=1608, role=cross_check)` |
| held-out eval policy | `heldout-eval-policy.md` | scorer/protocol role separation rule |
| hard-replace lexical | exec-plan E3b | `tmr_gt_pres_hard_replace_lexical_paired_acc = 0.6523 (n=512, role=diagnostic)` |
| condition manifest | `condition_manifest_summary.json` | `64` samples, `256` rows, observation only |
| G1/G2 attention observation | `g1g2_observation_analysis_summary.json` | `10240` records, entropy `0.9963`, role=diagnostic/router candidate |

## 5. Timeline

| 阶段 | 任务 | 预估 | 可否与 Paper B 并行 |
|------|------|------|-------------------|
| Week 1-3 | A-EXP1 多 baseline 诊断 | 2-3 周 | 可并行 B-EXP1 |
| Week 1-2 | A-EXP2 scorer-selection leakage | 1-2 周 | 可并行 B-EXP1 |
| Week 1 | A-EXP3 hard-negative replace | 1 周 | 可并行 B-EXP1 |
| Week 3-4 | A-EXP5 failure pattern | 1 周 | 可并行 B-EXP2 |
| Week 4-7 | A-EXP4 human eval（核心证据） | 2-3 周 | 可并行 B-EXP3 |
| Week 6-8 | 写作 | 2 周 | 可并行 B 写作 |

## 6. 独立成文条件

Paper A 完全不依赖 Paper B。所有实验都是 evaluation-side 的，不需要任何 reward guidance 结果。

如果 Paper B 先完成 guidance 实验，A 可以在 failure pattern 中加入"guidance 前后的 failure pattern 变化"作为 case study，但这不是必须的。

## 7. 当前禁写

1. 不把 EventProbe 写成新数据集论文。
2. 不把 `cross-evaluator consistency` 或 `open-source toolkit` 单独写成核心贡献。
3. 不把 `safe_drop_join`、`aligned_replace_manifest`、raw attention 或 MLLM sidecar 写成 standalone final evaluator。
4. 不把 `drop = ...`、`replace = ...`、`full>drop = ...` 裸写进论文表述；必须使用 README 中的 canonical metric name。
