---
created: 2026-04-29T23:37:35+08:00
updated: 2026-05-01T15:05:48+08:00
title: MoDebug Event-T2M Attention / Gradient Extraction Feasibility
status: archived
task_id: MDBG-ATTN-FEAS
tags:
  - MoDebug
  - EventT2M
  - attention-filter
  - feasibility
  - generation-observation
related_notes:
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-attention-filter-evaluator-pipeline-update]]"
  - "[[paperIDEAs/MoDebug/2026-04-30_modebug-render-video-mllm-sidecar-feasibility]]"
---

# MoDebug Event-T2M Attention / Gradient Extraction Feasibility

> [!warning] Archived
> This note is implementation support for attention / gradient instrumentation. It is not an active roadmap entry. Current MoDebug entry, terms, and active file list are in [[ideas/MoDebug/README]].

> [!abstract] **结论**
> Event-T2M 内部有可用的 event-token cross-attention 入口，适合做 G1/G2 的 observation 和 interval mining。该 feasibility 已被后续实现部分验证：G1/G2 opt-in attention logging 已完成并跑完 `256` condition rows；但 raw attention entropy 高、peak-order match 低，且 `observations.jsonl` 缺 per-head metric，所以仍只能作为 `Temporal Attention Filter` observation，不能写成 raw attention final judge。G3 feasibility 已确认，但 implementation 仍 pending；若不先补 per-head logging，G3 优先级低于 sidecar pilot。

## 1. 代码读取范围

只读输入：

1. `paperIDEAs/MoDebug/blocked/legacy_eventt2m/2026-04-29_modebug-exec-plan.md`
2. `paperIDEAs/MoDebug/blocked/legacy_eventt2m/2026-04-29_modebug-attention-filter-evaluator-pipeline-update.md`
3. `linkedCodebases/EventT2M-codes-main/src/models/nets/event_final.py`
4. `linkedCodebases/EventT2M-codes-main/src/models/event_final.py`

本 note 没有修改 Event-T2M 代码，没有跑 generation。

## 2. Decomposed Event Tokens 如何进入 Denoiser

事件条件链路是清晰的：

1. batch 中 `text` 结构被拆成 full caption 和 decomposed events。训练与评估入口都使用：
   - `decomposed = [[d['caption'] for d in t[1]] for t in text]`
   - 位置：`src/models/event_final.py:124`、`src/models/event_final.py:240`
2. `encode_decomposed_with_padding()` 将 event caption 列表 flatten 后送入 `text_encoder`，再 padding 到 `max_len=11`，输出：
   - `decomposed_embed["text_emb"]`: shape 语义上是 `[B, 11, clip_dim]`
   - `decomposed_mask`: `[B, 11]`，有效 event 为 `True`
   - 位置：`src/models/event_final.py:96-119`
3. diffusion training forward 调用：
   - `self.denoiser(x_t, padding_mask, timestep, text_embed, decomposed_embed, decomposed_mask)`
   - 位置：`src/models/event_final.py:143`
4. sampling 时 CFG batch 被扩成 conditional + unconditional：
   - full caption 扩展为空字符串作为 unconditional half
   - decomposed events 扩展为 `[[""] * 11] * B`
   - denoiser 输入 batch 是 `pred_motion.repeat([2, 1, 1])`
   - 位置：`src/models/event_final.py:280-307`
5. denoiser 内部先投影 full caption 和 decomposed events：
   - `text_tok = self.t_in(text_emb).unsqueeze(1)`
   - `decomposed_tok = self.t_in(decomposed_embed["text_emb"])`
   - `d_mask = decomposed_mask`
   - 位置：`src/models/nets/event_final.py:298-302`
6. 每个 `StageBlock` 都接收同一组 `decomposed_tok, d_mask`：
   - 位置：`src/models/nets/event_final.py:311-316`
7. `StageBlock` 会把 decomposed event tokens 用当前 stage 的 `y_proj` 投影到 stage dim：
   - `if d is not None: d = self.y_proj(d)`
   - 位置：`src/models/nets/event_final.py:217-219`
8. `MixedModule` 先把 motion sequence 去掉 time token 后做 patch-level local conv，再用 full caption token gate 注入全局文本，再进入 `MiniConformer`：
   - `seq = x[:, 1:]`
   - `seg = self.local_conv(...)`
   - `seg = self.inject_text(seg, y)`
   - `seg = self.global_conformer(seg, cross=d, cross_mask=d_mask)`
   - 位置：`src/models/nets/event_final.py:160-174`
9. `MiniConformer.cross_attn` 的 query 是 motion patch token `seg`，key/value 是 decomposed event tokens `d`：
   - `self.cross_attn(x, cross, cross, key_padding_mask=key_padding, need_weights=False)`
   - 位置：`src/models/nets/event_final.py:73-81`

因此，可解释的核心对象不是 frame-level raw attention，而是 **patch-level motion queries 对 decomposed event token keys 的 cross-attention**。patch 到 frame 的粗映射由 `patch_size` 决定，默认 `patch_size=8`，`seg_up = repeat(seg, "b l d -> b (l s) d", s=self.patch_size)` 再恢复到 motion length，位置：`src/models/nets/event_final.py:176-177`。

## 3. 可 Hook 的 MultiheadAttention 位置

### 3.1 `MiniConformer.mha`

位置：

1. 定义：`src/models/nets/event_final.py:28-30`
2. 调用：`src/models/nets/event_final.py:66-70`

含义：

1. query/key/value 都是 `seg`，即 patch-level motion tokens。
2. 它可以观察 motion patch 之间的 temporal self-attention。
3. 它不能直接回答某个 decomposed event token 对应哪个 temporal interval，因为 key/value 不是 event tokens。

可记录：

1. patch-to-patch attention entropy
2. temporal concentration / locality
3. denoising step 中 motion temporal dependency 的变化

### 3.2 `MiniConformer.cross_attn`

位置：

1. 定义：`src/models/nets/event_final.py:31-33`
2. 调用：`src/models/nets/event_final.py:77-81`
3. 上游传入：`MixedModule.global_conformer(..., cross=d, cross_mask=d_mask)`，位置 `src/models/nets/event_final.py:169-174`

含义：

1. query 是 patch-level motion tokens。
2. key/value 是 decomposed event tokens。
3. 这是 G1/G2 最关键 hook 点，可产生 `[batch, head, motion_patch, event_token]` 语义的权重。

可记录：

1. 每个 event token 被哪些 motion patches 查询。
2. 每个 motion patch 更依赖哪个 event token。
3. event token 的 temporal peak、top interval mass、entropy、order peak rank。
4. full / drop / replace / shuffle 条件下 cross-attention 是否发生方向正确变化。

### 3.3 `MixedModule.inject_text`

位置：`src/models/nets/event_final.py:145-148`

这不是 `MultiheadAttention`，但它把 full caption token 通过 gate 注入每个 patch token。它适合作为辅助 control signal，帮助区分 full-caption global bias 与 decomposed-event cross-attention；不应被写成 event-token attention。

## 4. 当前实现对 G1/G3 的限制

### 4.1 `need_weights=False` 限制 G1

两个 attention 调用都显式设置 `need_weights=False`：

1. self-attention：`src/models/nets/event_final.py:66-70`
2. cross-attention：`src/models/nets/event_final.py:77-81`

后果：

1. `self.mha(...)` 虽然写了 `out, attn = ...`，但 `attn` 会是 `None`，且没有被返回。
2. `self.cross_attn(...)[0]` 只取 attention output，不取 weights。
3. forward hook 只能看到 module output；在 `need_weights=False` 下看不到真实 weights。
4. 原样只能记录 hidden activations、output deltas、gate 值，不能记录 `attn_peak_t / attn_interval / event peak order`。

最小修复不是改模型行为，而是 instrumentation 开关：

1. 对 observation run 设置 `need_weights=True`。
2. 设置 `average_attn_weights=False`，保留 per-head 权重。
3. 只在 logging 模式收集，不进入正式 evaluator 结论。
4. 已完成的 `256` row observation 只落盘 head-averaged summary；若要做真正 per-head filtering，需要新增 per-head metric 字段并小规模重跑。

### 4.2 `@torch.no_grad()` 限制 G3

采样入口：

1. `sample_motion` 被 `@torch.no_grad()` 包住，位置：`src/models/event_final.py:280-281`
2. `encode_decomposed_with_padding()` 内部 text encoder 也在 `with torch.no_grad()` 中，位置：`src/models/event_final.py:102-103`
3. full caption training encode 也在 `with torch.no_grad()` 中，位置：`src/models/event_final.py:128-129`

后果：

1. 常规 `sample_motion()` 不能直接拿到 gradient sensitivity。
2. text encoder 参数不会有梯度；这本身合理，因为 G3 不应更新 backbone 或 text encoder。
3. 如果要做 G3，只能在一个窄作用域里重新启用 gradient，把 denoiser 冻住，把 `pred_motion` 或 `decomposed_embed["text_emb"]` 设为需要梯度，再做单步或少量 step 的 frozen forward。
4. G3 只能解释当前 denoiser 局部敏感性，不能说明最终生成一定包含该 event，也不能作为 final reward 或 judge。

## 5. 最小 Instrumentation Plan

目标是只回答 feasibility，不做 generation 质量 claim，不把 attention 写成 judge。

### Step 1：命名 hook 点

对每个 stage 注册名字：

```text
denoiser.layers.{i}.mixed.global_conformer.mha
denoiser.layers.{i}.mixed.global_conformer.cross_attn
denoiser.layers.{i}.mixed.inject_text gate
```

优先级：

1. 必做：`cross_attn`
2. 可选：`mha`
3. 辅助：`inject_text` gate

### Step 2：G1 Attention Map Observation

需要的 instrumentation：

1. `cross_attn` 返回 per-head weights。
2. 保存 stage、head、diffusion step、condition、sample id、event index。
3. 将 patch index 映射为 normalized time interval：`patch_idx * patch_size / motion_len`。
4. 对 full / drop / replace / shuffle 分别记录同一 event query 的 relative change。

G1 能记录：

1. `attn_peak_t`
2. `attn_interval`
3. `attn_mass_top_interval`
4. `attn_entropy`
5. `relative_gap_vs_generic`
6. `relative_gap_vs_corrupted`
7. `order_peak_rank`

G1 不能宣称：

1. attention peak 就是 event 真实发生位置。
2. peak order 就是 formal ordering metric。
3. raw attention 可以替代 TMR / ChronAccRet / human review。

### Step 3：G2 Denoising Trajectory Observation

需要的 instrumentation：

1. 在 sampling loop 的每个 scheduler timestep 记录 G1 同一组 attention summary。
2. 分开 conditional half 和 unconditional half；CFG batch 中前 `B` 是 conditional，后 `B` 是 unconditional。
3. 对每个 event 记录 peak emergence step、entropy decline、mass stabilization。

G2 能记录：

1. event attention peak 在哪些 denoising steps 出现。
2. late-emerge events 是否更容易 omission。
3. drop / replace / shuffle 是否改变 emergence pattern。
4. 哪些 steps 适合后续 intervention 观察。

G2 不能宣称：

1. trajectory signal 稳定前，不能进入 trajectory-aware guidance。
2. 单个 sample 的 emergence 顺序不能当成 ordering evidence。

### Step 4：G3 Gradient Sensitivity Observation

需要的 instrumentation：

1. 不调用默认 `sample_motion()` 全流程；写一个只读式 diagnostic forward 或在局部 `torch.enable_grad()` 中重放单步 denoiser。
2. 冻住 denoiser 参数。
3. 对 `pred_motion` latent 或 `decomposed_embed["text_emb"]` 开 `requires_grad_(True)`。
4. 选择固定 timestep 和 frozen generated motion / GT motion，计算 event-conditioned scalar，再反传得到 frame/patch gradient mass。
5. 比较 full / drop / replace / shuffle 的 gradient mass 和 temporal concentration。

G3 能记录：

1. event condition embedding 对 denoiser output 的 sensitivity。
2. latent frames / patch timesteps 上的 gradient mass。
3. condition corruption 是否改变 gradient localization。
4. event-specific sensitivity 是否集中到少量 temporal intervals。

G3 不能宣称：

1. gradient mass 高就代表 event 已发生。
2. gradient sensitivity 可以作为正式 evaluator。
3. raw gradient 可以直接变成 final reward。
4. text encoder token-level causality，因为当前 text encoder encode 是 no-grad；除非另做 embedding-level diagnostic。

## 6. Go / No-Go 判断

### Go 条件

1. `cross_attn` weights 可稳定取出，且不同 stage/head 不是全均匀或固定位置偏置。
2. GT / on-policy success 样本中，event peak temporal separation 明显强于 failure 样本。
3. drop / replace / shuffle 下，目标 event 的 relative attention 或 gradient mass 有方向正确变化。
4. G2 中至少部分 event 的 emergence pattern 可复现。
5. G3 在 frozen forward 中不需要更新 backbone，且梯度数值健康。

### No-Go / 只保留 logging 条件

1. 打开 `need_weights=True` 后显存或速度开销不可接受，无法覆盖 `40-80` 条 observation pool。
2. cross-attention 对所有 event 都集中在固定 early/middle/late patch。
3. shuffle 后 peak order 不变，drop 后目标 event attention 不降，replace 后 distractor margin 不变。
4. 不同 random seed / scheduler step 下 attention peak 大幅漂移。
5. gradient 主要反映 denoiser noise scale 或 padding artifact，而不是 event condition 差异。

## 7. 何时退回 Render-to-Video + MLLM Sidecar

以下情况不应继续硬挖内部 attention，而应退回 render-to-video + MLLM sidecar：

1. Event-T2M 内部 attention weights 无法低成本取出，或打开 `need_weights=True` 明显破坏采样吞吐。
2. `cross_attn` 只表现为 event-token prior，不随 motion latent / corruption 改变。
3. patch-level attention 太粗，无法区分相邻短事件，尤其是 `>=5 events` 的样本。
4. event 文本中的动作需要视觉语义验证，而 denoiser latent attention 不能对应到可解释 motion evidence。
5. G3 只能得到全局 gradient mass，不能定位到 temporal interval。
6. human quick review 与 attention interval 高频冲突。
7. 已有 observation artifact 缺 per-head metric，且短期不重跑 per-head logging。

sidecar 角色仍然是 temporal evidence extraction / routing support，而不是替代正式 evaluator。具体 pilot 见 [[paperIDEAs/MoDebug/2026-04-30_modebug-render-video-mllm-sidecar-feasibility|Render-to-Video + MLLM Sidecar Feasibility]]。

## 8. Temporal Attention Filter 的边界

本 feasibility 支持的模块边界与 [[2026-04-29_modebug-attention-filter-evaluator-pipeline-update]] 一致：

1. **observation layer**：记录 Event-T2M 内部 event condition 如何影响 patch-level denoising。
2. **interval miner**：为每个 event 产生候选 temporal interval。
3. **evaluator router**：把 high-entropy、low-margin、peak-order suspicious 的样本送给 TMR / ChronAccRet / human review / MLLM sidecar。
4. **future reward feature candidate**：只有 G1-G3 对 corruption 稳定敏感时，才考虑进入低权重 guidance MVP。

明确不承担：

1. 不作 raw attention final judge。
2. 不替代 ChronAccRet ordering evidence。
3. 不替代 TMR omission side signal。
4. 不把 event peak rank 写成 formal ordering metric。
5. 不在 held-out evaluator rule 明确前进入 reward-heavy guidance。

## 9. Feasibility Verdict

当前代码结构对 G1/G2 是 **中等可行但证据不足**：hook 点明确，`cross_attn` 正好连接 motion patch queries 与 decomposed event token keys；但当前落盘 artifact 没有 per-head metric，无法判断少数可用 head subset。

对 G3 是 **可行但需要单独 diagnostic path**：默认 sampling 是 no-grad，不能直接复用；但可以在 frozen denoiser 单步 forward 中局部启用 gradient，记录 embedding-level 或 latent-level sensitivity。

当前建议：

1. 若继续内部 attention path，先改 logging 保存 per-head entropy / mass / peak/order metric，再做小规模 `12-16` row probe。
2. 若 per-head probe 仍无 filtered entropy `< 0.95` 或 condition-order match 不稳定，停止内部 attention reward 路线。
3. 与其直接上 G3，不如并行准备 render-to-video + MLLM sidecar pilot；G3 只在 per-head 或 sidecar 给出可解释 temporal signal 后进入 implementation。
4. 无论选择哪条线，attention / sidecar 都只能作为 generation-side diagnostic 或 router，不进入 formal final evaluator。
