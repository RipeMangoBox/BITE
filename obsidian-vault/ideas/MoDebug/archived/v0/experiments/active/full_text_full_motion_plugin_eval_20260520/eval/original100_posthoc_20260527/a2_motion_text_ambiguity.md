---
title: Original100 motion-text ambiguity audit (a2)
type: diagnostic_note
date: 2026-05-27
updated: 2026-05-27T00:00
tags:
  - MoDebug
  - HumanML3D
  - Original100
  - text_ambiguity
  - status/diagnostic
---

# A2: Original100 motion-text 歧义整理

本轮对 Original100 的 100 条 sample 全量扫描了对应 HumanML3D text 文件，逐条比较 selected caption 与同一 motion 的全部 sibling captions。这里只落入队价值较高的可疑项；未入表的 motion 也已完成扫描，但没有发现足够强的 left/right、viewer-vs-actor、side/turn/circle/facing 相关自优化信号。

## 范围与原则

- 覆盖范围：Original100 全部 100 条 sample。
- 证据来源：sample manifest、`annotation_joined.jsonl`、以及 `linkedCodebases/datasets/HumanML3D/HumanML3D/texts` 下对应 motion 的全部 captions。
- 目标：识别同一 motion 内部 caption 是否互相矛盾、是否存在更清楚的 sibling caption、以及哪些条目适合进入“文本替换/补充”队列。
- 非目标：不把 train/test source 差异当作 held-out 贡献；这里只把它当诊断背景。

## 总结

- 全量扫描：100 / 100 motions。
- 入队条目：17 条。
- 优先级分布：high=12，medium=5。
- 动作分布：可直接替换 7 条；建议补充/自改写 4 条；建议保留或禁止自动替换 6 条。

## 主要歧义类型

1. `left/right` 在 sibling captions 内部互相冲突
   - 典型条目：`hml_orig100_train_010__full`、`hml_orig100_train_035__full`、`hml_orig100_test_007__full`、`hml_orig100_test_008__full`。
   - 这类条目不适合自动替换，因为同一 motion 的不同文本已经把核心 side assignment 说反了。

2. 选中的文本太短，路径/转向细节被压扁
   - 典型条目：`hml_orig100_train_004__full`、`hml_orig100_train_013__full`、`hml_orig100_train_016__full`、`hml_orig100_train_066__full`。
   - 这类 motion 往往存在更清楚的 sibling caption，能补上 quarter-circle、counter-clockwise、360-degree、facing forward 等关键信息。

3. viewer-centric 参照系混入文本
   - 典型条目：`hml_orig100_train_063__full`、`hml_orig100_train_079__full`。
   - 问题不在 motion 本身，而在文本用了 `viewer` 或等价的镜头参照系，适合作 actor-centric 自改写。

4. selected caption 已较清楚，但 sibling captions 语义发散过大
   - 典型条目：`hml_orig100_train_002__full`、`hml_orig100_train_065__full`。
   - 这类条目更适合作为“禁止从 sibling 自动挖替换文本”的黑名单，而不是替换候选。

## 可自优化策略

1. 可直接替换
   - 只在 sibling caption 提供了更完整但不改核心语义的 path / facing / turn 细节时使用。
   - 当前高价值条目包括：`train_004`、`train_013`、`train_063`、`train_066`、`test_009`、`test_016`。

2. 只做补充或自改写
   - 适用于 selected caption 大体正确，但可增加 actor-centric framing，或去掉 viewer-centric phrasing。
   - 当前典型条目：`train_001`、`train_007`、`train_016`、`train_074`、`train_079`。

3. 禁止自动替换
   - 适用于 sibling captions 在 left/right、kick leg、pick/place side 等核心属性上互相冲突。
   - 当前典型条目：`train_002`、`train_010`、`train_035`、`train_065`、`test_007`、`test_008`。

## 输出文件

- `a2_motion_text_ambiguity.tsv`：每个入队 motion 一行，包含 selected text、同 motion 全部 captions、歧义理由、更清楚 sibling captions、建议动作、受影响 baseline、GT 是否也有问题、优先级。
- 本 note 作为中文诊断摘要，供后续自优化文本替换/补充流程引用。

## 备注

- 这里的 `affected_baselines_with_problem` 只是帮助排序，不代表文本歧义必然是问题根因。
- 对于存在 sibling conflict 的 motion，后续若要真的替换文本，最好先结合视频或原 motion 可视化做人工复核。

