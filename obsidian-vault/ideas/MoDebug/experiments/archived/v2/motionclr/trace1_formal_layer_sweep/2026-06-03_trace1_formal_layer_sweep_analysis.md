---
title: "Trace1 Formal Layer Sweep Analysis"
created: 2026-06-03T16:06:29+08:00
updated: 2026-06-03T16:45:02+08:00
status: diagnostic_completed
hypothesis: "MotionCLR 的文本条件传播敏感层集中在早期 L0-L3 与后段 L12-L15；该证据只支持机制诊断，不支持 paper-level 指标。"
source_papers: []
tags:
  - MoDebug
  - trace_1
  - formal_diagnostic
  - layer_sweep
---

# Trace1 Formal Layer Sweep Analysis

> [!abstract] 结论
> Trace 1 formal diagnostic 已完成用户要求的两类 18 层逐层测试：CA output suppression 和 CFG hidden replacement，各 18 个 layer group；按 3 个 seeds 展开后各 54 行结果。controls 通过，`failures=[]`。这支持“MotionCLR 文本条件传播的数值敏感层”判断，但不支持 FID、R-Precision、语义质量或 paper-level performance claim。

## Run 与边界

| 项目 | 值 |
|------|----|
| run dir | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_formal_layer_sweep_ds_review_20260603_gpu1/` |
| scope | `formal_diagnostic_layer_sweep` |
| paper-level status | `not_final_full_evaluator_result` |
| summary SHA256 | `17296bab4e3ec2d59f5cae6c921b6c2002a66b039fff15f280228238edabee5b` |
| layers | 18 |
| seeds | `0, 1, 2` |
| prompts per seed | 64 |
| denoise steps | 10 |
| CFG scale | 2.5 |
| CA alpha | 0.0 |
| elapsed | 524.16 秒 |

本页结论经 DS 复核，verdict 为 `APPROVED_WITH_CAVEATS`。DS 要求把“切断文本条件传播”的强因果表述降级为“在该 hook 和采样设置下产生更大的隐空间输出差异”，并保留 L2 指标、固定采样配置、未做 official evaluator 的边界。

## 完整性与 controls

| family | 行数 | 解释 |
|--------|------|------|
| baseline | 3 | 每个 seed 一个未扰动 baseline。 |
| noop | 6 | 两类 no-op，各 3 seeds。 |
| positive_control | 6 | 两类 all-layer positive control，各 3 seeds。 |
| ca_output_perturbation | 54 | 18 层 × 3 seeds，逐层 CA output suppression。 |
| cfg_hidden_replacement | 54 | 18 层 × 3 seeds，逐层 cond-half hidden 替换为 uncond hidden。 |

controls 结果：

- `noop_ca_all_layers_alpha_1` 与 `noop_hidden_hook_all_layers_disabled` 在 3 个 seeds 上均 `allclose_vs_baseline=True`，`max_abs_vs_baseline=0`。
- `positive_control_ca_all_layers_alpha_0p0` 与 `positive_control_hidden_replace_all_layers` 在 3 个 seeds 上均 `allclose_vs_baseline=False`，`max_abs_vs_baseline` 分别约为 147.27、61.63、79.15。
- positive controls 的 `max_pre_cfg_delta=0`，说明 all-layer 操作把 CFG 条件半边与无条件半边的 pre-CFG 差异压到零，符合预期。

## 主结果

整体 L2 vs baseline：

| family | mean L2 | min L2 | max L2 |
|--------|---------|--------|--------|
| CA output suppression | 524.50 | 52.82 | 1510.48 |
| CFG hidden replacement | 993.25 | 136.17 | 2627.41 |

![[figures/motionclr_trace1_layer_mean_l2.svg]]

逐层均值：

| Layer | CA output suppression mean L2 | CFG hidden replacement mean L2 | 备注 |
|-------|-------------------------------|--------------------------------|------|
| L0 | 1414.38 | 1414.38 | 两类 hook 完全相同；见 L0 caveat。 |
| L1 | 1172.08 | 1815.36 | 早期高敏感。 |
| L2 | 793.39 | 1191.38 | 早期高敏感。 |
| L3 | 616.76 | 1280.90 | 早期高敏感。 |
| L4 | 248.24 | 583.50 | 中低响应。 |
| L5 | 125.73 | 592.64 | CA 低响应，CFG 中等响应。 |
| L6 | 104.23 | 167.59 | 低响应。 |
| L7 | 65.30 | 160.28 | 低响应。 |
| L8 | 147.00 | 231.02 | 低响应。 |
| L9 | 98.36 | 247.70 | 低响应。 |
| L10 | 306.01 | 687.36 | 中等响应。 |
| L11 | 317.76 | 749.82 | 中等响应。 |
| L12 | 1253.75 | 1652.88 | 后段高敏感。 |
| L13 | 849.31 | 1744.88 | 后段高敏感。 |
| L14 | 953.90 | 2431.20 | CFG peak 区域。 |
| L15 | 764.71 | 2608.90 | CFG peak。 |
| L16 | 105.94 | 146.97 | 低响应。 |
| L17 | 104.14 | 171.75 | 低响应。 |

## 解释

1. **36 个逐层 layer group 已完成**：CA output suppression 有 18 个 layer group，CFG hidden replacement 有 18 个 layer group；3 seeds 展开后共 108 行逐层结果。gpu1 空闲可以解释为 Trace 1 formal diagnostic 已跑完，而不是 Trace 3 完成。
2. **敏感层呈双簇分布**：L0-L3 与 L12-L15 的平均 L2 明显高于 L6-L9、L16-L17。这支持将早期层和后段层视作当前 MotionCLR 采样链中的文本条件传播敏感区域。
3. **CFG hidden replacement 的 L2 更大，但不可直接等价为更强因果切断**：该干预替换的是整层输出 hidden state，范围大于只压制 cross-attention 输出；因此只能说它在本配置下造成更大的输出差异，提示更高敏感性，不能直接声称“更强地切断文本条件”。
4. **L0 是特殊边界点**：原始 3 个 seed 的 L0 两类 hook 行完全相同，已核对不是汇总转录错误。代码层面的合理解释是，CFG 双半边在第一层前 motion latent 和 timestep 相同，差异主要来自文本条件分支；在 L0 上 CA 输出归零与把 cond hidden 替换为 uncond hidden 会把后续状态推进到同一数值轨迹。因此 L0 可作为“首层条件差异被抹除”的边界证据，但不应作为比较两类干预强弱的独立证据。
5. **低响应层不等于不重要**：L6-L9、L16-L17 只是在这两种 hook 与该采样设置下的 L2 响应较小，不能推断这些层对生成质量或语义一致性没有作用。

## 结论与下一步

Trace 1 当前可写入研究记录的结论是：MotionCLR 的文本条件传播数值敏感区集中在 L0-L3 与 L12-L15，CFG hidden replacement 在多数层上产生比 CA output suppression 更大的 output-space delta；其中 L14-L15 是 CFG replacement 的最强响应层，L12 和 L0-L1 是 CA output suppression 的最强响应层。

后续 Trace 1 若继续做 intervention/readout，优先候选层为 L0-L3 与 L12-L15；其中 L0 单独作为首层边界点处理，L12-L15 更适合作为后段干预重点。任何语义质量判断必须再接 qualitative motion inspection、official evaluator subset 或 full evaluator，不能从本页 L2 表直接推出。

必须保留的 caveat：

- L2 是 normalized motion feature array 与 baseline 的数值差异，不是运动质量、文本对齐或人类偏好指标。
- 本实验固定为 3 seeds、64 prompts、10 denoise steps、CFG scale 2.5、一个 MotionCLR release checkpoint；其他采样步数、CFG scale 或 checkpoint 不保证同样排序。
- CA output suppression 与 CFG hidden replacement 的干预范围不同，二者 L2 大小不可作为同一量纲的因果强度比较。
- 本实验没有 FID、R-Precision、多模态距离或人工评分，不能形成 paper-level performance claim。
