---
created: 2026-04-27T16:35
updated: 2026-04-27T16:35
title: MoDebug Plan B：FineMotion Weak-Supervision Audit
status: archived
tags:
  - MoDebug
  - plan-b
  - FineMotion
  - weak-supervision
  - body-part
related_notes:
  - "[[dataset_readiness_manifest_v1]]"
  - "[[2026-04-25_modebug-pivot-implicit-event-repair]]"
---

# MoDebug Plan B：FineMotion Weak-Supervision Audit

## 0. 本审计回答什么

这里只回答一个问题：

> 当前 `FineMotion` 文本标注根里，哪些字段适合做 **body-part weak supervision / error analysis / R_pres sidecar**，哪些不适合进入 Plan B 主线 reward？

结论先行：

- **适合进入 sidecar**：`BPMSD_human.json`、`BPMSD_auto.json`
- **适合做段落级参考，不适合主线 reward**：`BPMP_human.json`、`BPMP_auto.json`
- **不建议进入当前主线 reward**：任何需要严格单标签 body-part ground truth 的用法

## 1. 当前可用文件

当前 standalone `FineMotion` 文本标注根：

- `/home/ripemangobox/Coding/Github/Motion/datasets/FineMotion/BPMP_auto.json`
- `/home/ripemangobox/Coding/Github/Motion/datasets/FineMotion/BPMP_human.json`
- `/home/ripemangobox/Coding/Github/Motion/datasets/FineMotion/BPMSD_auto.json`
- `/home/ripemangobox/Coding/Github/Motion/datasets/FineMotion/BPMSD_human.json`

其中：

- `BPMSD_*`：0.5s snippet-level 描述
- `BPMP_*`：整段 paragraph-level 描述

## 2. 结构层面的第一结论

### 2.1 BPMSD 更适合 Plan B

原因很简单：

- Plan B 的主单位是 `event / local interval`
- `BPMSD` 本身就是片段级
- 它天然可以拿来做：
  - body-part 提及检测
  - local evidence caption 候选
  - error analysis tag

而 `BPMP` 是整段段落，虽然可读性高，但太粗，不适合直接拿来做局部 reward。

### 2.2 human 优先于 auto

当前最稳的优先顺序应当是：

1. `BPMSD_human.json`
2. `BPMSD_auto.json`
3. `BPMP_human.json`
4. `BPMP_auto.json`

## 3. 当前能直接读出的弱监督强度

基于本地快速词面统计，`BPMSD_human.json` 当前有：

- 非空 snippet 数：`18768`
- 多标签倾向 snippet 数：`11850`

显式 body-part / 区域提及频次：

| 标签 | 提及数 |
| --- | ---: |
| `LOWER_BODY` 倾向 | `11514` |
| `LEFT_ARM` 倾向 | `7942` |
| `RIGHT_ARM` 倾向 | `7942` |
| `UPPER_BODY` 倾向 | `7814` |
| `BOTH_ARMS` 倾向 | `2398` |

直接结论：

- `LOWER_BODY` 是最容易拿到稳定弱标签的
- `LEFT_ARM / RIGHT_ARM` 次之
- 大量 snippet 同时提多个 body region，因此它不适合硬做单标签分类真值

## 4. 哪些字段最适合做什么

### 4.1 最适合做 body-part weak supervision 的

**首选：`BPMSD_human.json`**

适合做：

- `body-part mention` 二值弱标签
- `left vs right vs lower-body` 的弱区分
- 错误分析时的局部文字证据

不适合做：

- 严格单标签 supervised body-part classifier ground truth
- 直接作为 Plan B 主 reward 的 hard target

### 4.2 最适合做 coverage 扩展的

**次选：`BPMSD_auto.json`**

适合做：

- 扩 coverage
- 挖更多部位-动作组合词表
- 做弱规则词典或 retrieval support

不适合做：

- 主线定量结论
- 任何需要高精标签的评测集

### 4.3 最适合做 error analysis / explanation 的

**`BPMP_human.json` + `BPMP_auto.json`**

适合做：

- 阅读型 error analysis
- 人看结果时的 qualitative explanation
- 将来若做 Observer-Solver 路线时的 evidence template 参考

不适合做：

- 当前 Plan B 的局部 reward
- 片段级 hard negative 判断

## 5. 对 Plan B 的直接用法建议

### 5.1 现在就可以做的

1. 把 `BPMSD_human.json` 当成 **body-part sidecar**
2. 只做 `mention-level weak labels`
3. 服务于：
   - `error analysis`
   - `R_pres` sidecar 对照
   - 将来 `Motion-PRCO` 的 evidence style 参考

### 5.2 现在不要做的

1. 不要把 `FineMotion` 拉进当前主线 reward
2. 不要把 `BPMSD_human.json` 当作 clean single-label GT
3. 不要让 body-part weak supervision 抢 `ordering / omission` 主线的资源

## 6. 最终判断

对当前 MoDebug Plan B 来说，`FineMotion` 的正确位置是：

- **不是主线 reward 数据源**
- **是 body-part / local evidence 的 sidecar 弱监督源**

一句话收口：

> `FineMotion` 现在最有价值的不是帮你定义主线 `R_pres / R_ord / R_dur`，而是作为一个 **body-part weak-supervision + qualitative error-analysis reservoir** 挂在 Plan B 旁边。 
