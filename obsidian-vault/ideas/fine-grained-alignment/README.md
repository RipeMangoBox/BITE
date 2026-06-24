---
title: "MLPA README"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-26T22:44:25+08:00
status: active
hypothesis: "MLPA 通过构造文本局部单元与 motion 时间、身体部位、接触线索之间的可审计对应层，降低 text-motion alignment 难度。"
tags:
  - MLPA
  - fine_grained_alignment
  - index
  - canonical
---

# MLPA README

## 标准名称

**MLPA** = **Multi-Level Pivot Alignment**。

当前完整定位：

```text
MLPA: Multi-Level Pivot Alignment for Event-Time-Body Correspondence in Text-to-Motion Generation
```

## 当前定位

MLPA 不是“换更强 text embedding”，也不是 motion generator 的失败诊断分支。它的核心是构造一个模型外部、可审计、可复用的局部对应层：

```text
text event / body phrase / temporal attribute
<-> motion temporal chunk / body-part token / root-contact cue
```

这个对应层可服务五类下游：

1. event-guided motion timestamping；
2. frozen candidate rerank；
3. verifier / guidance；
4. 后续轻量 generator conditioning；
5. 若前置关口通过，扩展为 pivot-level scaffold -> fine-grained event motion 的生成阶段。

其中 `scaffold` 不是泛泛的 plan。当前采用两级定义：

1. **Verification scaffold**：text unit、candidate time window、body-part group、root/contact/velocity cue、order constraint、null / ambiguity 和 evidence trace，用于 timestamping、rerank 与 verifier。
2. **Generation scaffold**：event windows、body-part activity map、root/contact cue map、duration/order constraints、low-confidence regions 和 transition slots，用于后置 pivot-first generation。

因此 pivot-first generation 是后置扩展，不是第一版主 claim。第一版先隔离验证 correspondence layer 是否真实有效。

## 停滞症结

MLPA 之前停滞在“跨领域类比很多，但没有落成 motion-specific operator”。3DGS、triplane、MLLM 的价值不在于写成灵感段落，而在于抽象出可执行机制：

1. 3DGS 启发显式 pivot、coverage、uncertainty 和局部 densification。
2. Triplane 启发 `time × body`、`time × text unit`、`body × attribute/contact` 的低维交互面。
3. MLLM / A.I.R. 启发 query-aware evidence acquisition，即围绕文本单元找局部证据，而不是全视频自由 caption。
4. Span-level alignment 启发 counterfactual locality，让 drop / replace / shuffle / mask-part 能验证对应关系是否真实。

## 与 MoDebug 的边界

| 方向 | 研究对象 | 主要证据 | 方法输出 |
| --- | --- | --- | --- |
| MoDebug | 文本条件在生成器内部如何传播并影响 motion | trace signal + guided output cross-check | propagation signature 与 guidance |
| MLPA | 文本局部单元与 motion 时间、身体部位、接触线索如何对应 | correspondence score + timestamp / rerank check | event-time-body correspondence layer |

两者可以共享 hard prompts、文本扰动和人工检查规范，但不能共享主 claim。

## 当前结构

1. [[ideas/fine-grained-alignment/roadmap|MLPA 当前路线图]]
2. [[ideas/fine-grained-alignment/mechanism_transfer/README|跨领域机制迁移笔记]]
3. [[gates|实验关口]]
4. [[2026-05-18_multi-level-pivot-alignment|早期主笔记]]
5. [[2026-05-19_multi-agent-consultation-and-molingo-audit|多 agent 顾问与 MoLingo 审计]]
6. [[2026-05-24_pivot-first-generation-route|Pivot-First Generation Route]]
7. [[2026-05-26_kimodo-seed-humanml3d-data-route|Kimodo/SEED 与 HumanML3D 双轨数据路线]]
8. [[2026-05-26_molingo-sae-and-posefix-sidecar-route|MoLingo TPA-SAE and PoseFix Sidecar Route]]

## 当前数据路线

MLPA 的主事件对齐证据切到 **Kimodo / BONES-SEED / SEED-Timeline**。原因是 Qwen3-VL-Plus 对 HumanML3D 完整视频做 event captioning 或 grounding 时，event 粒度和时间定位都不稳定；这些输出不能作为 ground truth。

当前采用双轨：

1. **Kimodo/SEED 主线**：使用官方 timeline event segment 与文本描述，优先支持 timestamping、rerank、verifier 和后续 scaffold gate。
2. **HumanML3D/HumanML3D-E 支线**：保留为 baseline-rich 的快速诊断、failure bank、PoseFix/FineMotion-style weak body-part sidecar、窗口级 VLM pseudo-label 和工程 smoke，不进入 final evaluator。
3. **MoLingo TPA-SAE 分支**：作为 generator-backbone retraining candidate，先验证 Temporal-Phrase Alignment 是否改善 SAE latent / downstream generation；它不是 MLPA 第一阶段主 claim。

2026-05-26 4090 状态：MoLingo 已开远端 `TPA` 分支，当前有效 head 为 `45a3f2f`。已完成 `wm / tpa_abspos / token_sentence` 三种 SAE semantic loss mode 的最小实现、semantic loss 聚合修复、fixed debug smoke 和 DeepSeek blocking-bug 复核；`45a3f2f` 前两个 short diagnostic 因 raw semantic loss 误入 total loss 作废。两个 fixed `batch_size=16, max_epoch=5` short diagnostic 已完成并生成 `checkpoint-last.ckpt`，初始 `MPJPE=145.5051`、`FID=683.7445`，观测训练显存约 `2.3GB/GPU`，日志未检出 fatal error；但本次没有 final eval 或中途 eval 曲线。该分支仍是 `diagnostic`，不进入 MLPA final evaluator 或正式排序证据。详见 [[2026-05-26_molingo-sae-and-posefix-sidecar-route|MoLingo TPA-SAE and PoseFix Sidecar Route]]。

后续不再依赖非官方数据切分做实验或验证。若需要小规模调试，只能从 Kimodo official train split 生成 disposable cache，并明确不进入 final evaluation。

## 当前阶段顺序

1. **MVP-0：Data Contract**。确认 event text、motion path、timestamp 来源、split 角色和 evaluator 角色；Kimodo/SEED 作为主线，HumanML3D/Qwen 只作 diagnostic。
2. **MVP-A：Timestamping / Correspondence**。验证 ordered text units 是否能定位 motion chunks，并记录 null / ambiguity / evidence trace。
3. **MVP-B：Frozen Rerank**。验证 local correspondence score 是否能改善候选 motion 选择，而不只是提升自身分数。
4. **MVP-C：Verifier / Guidance Readiness**。只允许 verifier、rerank、low-confidence chunk resampling、small adapter 或 masked cross-attention gating。
5. **MVP-D：Pivot-First Generation Extension**。在 A/B/C 有正信号后，才进入 generation scaffold -> motion detail refiner。

## 当前禁区

1. 不把 MLPA 写成 MoDebug 的 text embedding 分支。
2. 不把 3DGS / triplane 写成几何等价类比；只保留可迁移机制。
3. 不宣称首次 semantic latent alignment、event-level generation、part-level control 或 late interaction。
4. 不让 MLLM / VLM 直接成为 final evaluator。
5. 不在 timestamping 关口通过前训练大 generator。
6. 不把 pivot-first generation 写成第一阶段主 claim；它必须以后置 gate 的形式出现。
7. 不把 BABEL frame / segment labels 写成完整 event-time-body ground truth；BABEL 可支持 event-time anchor，但 body-part correspondence 仍需额外证据或验证。
8. 不使用非官方数据切分做正式实验、验证或 pilot；调试 cache 必须来自 official train split 且不参与 final evaluation。
9. 不把 Qwen / VLM 自动输出写成 motion event ground truth 或 final evaluator。
10. 不把 PoseFix / FineMotion-style 自动片段描述写成动态 event boundary ground truth；它只能是 weak body-part evidence 或 diagnostic sidecar。
11. 不把 MoLingo SAE retraining 的内部 cosine / temporal-semantic side signal 写成 MLPA final evaluator。
