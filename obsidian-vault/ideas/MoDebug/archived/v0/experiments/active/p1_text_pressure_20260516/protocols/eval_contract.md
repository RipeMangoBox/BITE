---
title: "MoDebug P1 Text-Pressure 诊断协议"
created: 2026-05-16T21:45:00+08:00
updated: 2026-05-20T13:45:48+08:00
tags:
  - MoDebug
  - P1
  - text_pressure
  - diagnostic
---

# MoDebug P1 Text-Pressure 诊断协议

## 目标

定义 P1 text-pressure set 的输出边界：当前 active 结果只说明文本侧 full-vs-single pressure 和 P1 generator/motion 缺失状态，不作为生成器传播、动作语义正确性或最终评估器证据。

## 数据对象

- `inputs/sample_manifest.tsv`：10 个 full prompt sample。
- `inputs/event_decomposition.tsv`：30 个 decomposed event。
- `inputs/single_event_prompt_manifest.tsv`：30 条 single-event prompt。
- `eval/text_embedding/`：CLIP text embedding diagnostic。
- `eval/text_embedding_ext/`：DistilBERT / T5 / Qwen text embedding diagnostic。
- `eval/generator_propagation/p1_missing_generator_trace.tsv`：P1 trace 缺失表。

## 计算方式

1. 文本侧：比较 full prompt embedding 与 single-event prompt embedding。
2. 多 encoder 复查：只用于检查 P1 text-pressure 是否依赖单一 encoder。
3. 缺失数据：发现 P1 trace 或 motion 缺失时写 missing report；不硬补、不伪造、不使用旧 proxy。

## 必需元数据

每个结果文件必须包含或在报告中声明：

- date
- artifact_path 或 experiment_path
- evaluator
- protocol
- data_source
- prompt_pair 或 condition_pair
- n/evaluable
- coverage
- role
- used_for
- limitations

## 允许结论

1. P1 输入集是否覆盖指定 event_count / target_dimension。
2. full prompt 与 single-event prompt 在文本 encoder 下的相似度或距离。
3. 某个 encoder 的 finite coverage 是否足够。
4. P1 generator trace、generated motion 或 motion-side satisfaction 是否缺失。
5. 后续补实验队列如何排序。

## 禁止事项

1. 不把 embedding distance、attention、similarity、VLM、geometry check 写成 final evaluator。
2. 不把旧 M0 proxy 当成 P1 generator/motion 侧结果。
3. 不把“event embedding 在 propagation 中稳定保留”写成未经 motion satisfaction 验证的必要条件。
4. 不把 P1 文本侧趋势写成 instruction-following 提升。
5. 不用本目录结果替代 full-text / full-motion plugin evaluation。

## 结论边界

本协议只允许把当前输出解释为文本侧诊断观察或缺失报告。若要形成 MoDebug 方法结论，需要在 `active/full_text_full_motion_plugin_eval_20260520/` 中补齐 `B` vs `B+MoDebug` 的 paired full-motion evidence。
