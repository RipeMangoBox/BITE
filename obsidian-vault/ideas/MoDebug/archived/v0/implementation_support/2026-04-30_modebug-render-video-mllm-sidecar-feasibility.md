---
created: 2026-04-30T01:15:00+08:00
updated: 2026-05-01T15:05:48+08:00
title: MoDebug Render-to-Video + MLLM Sidecar Feasibility
status: archived
task_id: MDBG-MLLM-SIDECAR-FEAS
tags:
  - MoDebug
  - feasibility
  - generation-observation
  - mllm-sidecar
  - render-to-video
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-attention-filter-evaluator-pipeline-update]]"
  - "[[2026-04-29_modebug-attention-extraction-feasibility]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
---

# MoDebug Render-to-Video + MLLM Sidecar Feasibility

> [!warning] Archived
> This note is implementation support for a generation-side diagnostic sidecar. It is not a formal evaluator or active roadmap entry. Current MoDebug entry, terms, and active file list are in [[ideas/MoDebug/README]].

> [!abstract] **结论**
> render-to-video + MLLM sidecar 可以作为 attention filtering 失败后的 Plan B，但只能定位为 `generation-side diagnostic / evaluator router / human-review prioritizer`。它不进入 formal final evaluator、reward scorer、main-table judge 链路；除非后续单独做人类校准并写清 held-out protocol，否则不能把 MLLM verdict 当最终论文指标。

## 1. 复查现有定位

当前 active MoDebug 文档对 sidecar 的描述很窄：

1. [[2026-04-29_modebug-roadmap|Roadmap]] 固定正式主线为 `Event-T2M + HumanML3D-E + inference-time event-level reward guidance`，并明确 `MotionPatches` 不进入任何正式 eval / scorer / judge 链路。
2. [[2026-04-29_modebug-attention-filter-evaluator-pipeline-update|Attention Filter Pipeline Update]] 写明：优先从 Event-T2M 内部提取 motion-native attention；若内部 attention 不稳定，再走 `render-to-video + MLLM attention sidecar`。sidecar 的目标是 escalation / routing，不是 final metric。
3. [[2026-04-29_modebug-exec-plan|Exec Plan]] 已有 G1/G2 结果：`256` condition rows、`10240` attention records、`0` finite failure，但 raw attention entropy 高、condition-order peak match 低，且现有 artifact 缺 per-head metric。下一步是 per-head logging 小重跑或 render-to-video MLLM sidecar，仍不进入 reward。
4. [[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]] 固定硬规则：reward scorer/protocol 不能同时作为 final main-table evaluator/protocol。MLLM sidecar 若被用于开发期筛样或 prompt tuning，也不能再作为同一 claim 的最终 judge。

因此，本 note 只补 Plan B 的落地性，不改变正式 evaluator 栈。

## 2. 目标与非目标

目标：

1. 在 attention filtering 不能给出稳定 event interval / corruption sensitivity 时，提供一个可读、可复查的视觉诊断侧车。
2. 把 `HumanML3D-E generated motion` 渲染成短视频或 grid，让 MLLM 回答 event presence、coarse order、obvious mismatch 等问题。
3. 为 `full / drop / replace / shuffle` corruption family 生成 side evidence，帮助决定哪些样本送 TMR、ChronAccRet 或人工复核。
4. 输出结构化 jsonl，服务 generation-side diagnostic 和 roadmap 风险判断。

非目标：

1. 不作为 formal final evaluator。
2. 不作为 main-table judge。
3. 不接入 reward / scorer / judge 链路。
4. 不替代 HumanML3D-E、TMR、ChronAccRet 或 Event-T2M self eval。
5. 不引入 MotionPatches 到正式链路。

## 3. 最小 Render Pipeline

输入固定为 HumanML3D-E 主数据口径：

```text
HumanML3D-E ordered events
  -> Event-T2M generated motion or GT motion
  -> recover / skeleton render / optional SMPL render
  -> short video or multi-view grid
  -> MLLM sidecar diagnostic
```

最小实现优先级：

1. **Skeleton render first**  
   优先使用 HumanML3D / Event-T2M 已有的 recover-to-joints 或 plot skeleton 工具，把 `263-dim motion` 恢复到关节轨迹后渲染。先不要追求 SMPL mesh 质感；视觉可读性比 photorealism 更重要。

2. **Short video + contact sheet**  
   每条 motion 输出一个 4-8 秒短视频，并额外输出 `8` 或 `12` 帧 grid。视频用于 temporal order；grid 用于成本更低的 presence / rough order 问答。

3. **Consistent camera and normalization**  
   固定视角、地面平面、人物尺度、帧率、颜色编码。避免因为 camera jump 或自动缩放让 MLLM 把渲染 artifact 误判成动作差异。

4. **Optional SMPL only after skeleton works**  
   如果 skeleton 对细粒度身体部位动作不可读，再考虑 SMPL / mesh render。SMPL 会引入恢复失败、身体形状、渲染依赖和延迟，不应作为 pilot 的第一依赖。

5. **No long experiment**  
   pilot 只渲染小样本，不跑新训练，不改 Event-T2M / ChronAccRet 源码。

## 4. MLLM 候选与接口风险

候选分三层：

1. **GPT-4o / GPT-4o-class video or image API**  
   优点是视觉问答稳定、结构化输出能力强，适合先做小样本 feasibility。风险是成本、速率限制、模型版本漂移、视频输入规格变化，以及不可完全复现实验环境。

2. **Gemini video / image API**  
   优点是长视频和多帧理解能力可能更强，可作为 cross-check。风险同样是 API 版本漂移、区域和额度限制、输出格式偶发不稳定。

3. **本地 VLM / Video-LMM**  
   可选 Qwen2.5-VL、InternVL、LLaVA-Video 一类本地模型。优点是可复现、可批处理、成本可控；风险是对 skeleton render 的动作语义理解可能弱于闭源 MLLM，需要更多 prompt engineering 和人工校准。

接口风险：

1. 视频输入常有时长、大小、帧率限制；pilot 应保留 grid fallback。
2. MLLM 对 skeleton stick figure 的先验不一定稳定；prompt 必须明确这是 3D skeleton motion render。
3. 输出需要强制 JSON schema，并保留 raw response 供人工 audit。
4. 同一模型版本需要记录 `provider / model / date / input_type / prompt_hash / temperature / seed_if_any`。
5. 不同 MLLM 的分歧不能自动平均成最终分数，只能作为 sidecar disagreement signal。

## 5. Corruption Family 对接

sidecar 不需要一次性覆盖所有语义，只需要围绕 MoDebug 当前 corruption family 设计窄问题。

### 5.1 Full

输入：原始 ordered events + generated motion render。

视觉问答：

1. `Does the video show all listed events at least approximately?`
2. `Which events are visually missing or unclear?`
3. `Give a coarse temporal order of visible events.`

输出字段建议：

```yaml
condition: "full"
visible_events: [0, 1, 3]
unclear_events: [2]
missing_events: []
coarse_order: [0, 1, 2, 3]
confidence: 0.62
failure_tags:
  - unclear_middle_event
```

### 5.2 Drop

输入：full text 与 drop text 的 pair，或 drop condition 对应 render。

pairwise judge 问题：

1. `Which prompt better matches the video: full or drop?`
2. `Is the dropped event visually present in the video?`

预期用途：检查 MLLM 是否能发现 omission，而不是生成正式 omission 分数。

### 5.3 Replace

输入：full event、replaced event、render。

视觉问答：

1. `Does the video match the original event or the replacement event better?`
2. `Is the distinguishing body action visible?`

风险：replace 常依赖细粒度语义，skeleton render 可读性可能不足。pilot 中 replace 只作为 hard diagnostic，不作为 Go 的唯一依据。

### 5.4 Shuffle

输入：原始 ordered events、shuffled events、render。

pairwise judge 问题：

1. `Which event order is more consistent with the video?`
2. `List the observed event order using event ids.`

预期用途：作为 ordering disagreement side evidence，帮助决定是否送 ChronAccRet 或人工复核。它不能替代 ChronAccRet formal ordering evidence。

## 6. 成本、延迟与可复现风险

主要风险：

1. **成本**：闭源 MLLM 视频输入比图像 grid 昂贵。`64 samples x 4 conditions` 会变成 `256` 个调用，若每条还做 pairwise prompt，成本会快速上升。
2. **延迟**：视频上传和推理慢，不适合 inner-loop reward guidance。sidecar 应离线批处理，只用于 observation / routing。
3. **可复现**：API 模型版本、视频编码、采样温度和 prompt 细节都会影响输出。必须记录模型版本、prompt hash、输入文件 hash。
4. **视觉偏差**：MLLM 可能更擅长自然视频，不擅长 skeleton。需要加入 skeleton-specific instruction，并用少量人工标注校准。
5. **prompt leakage**：如果把 full/drop/replace/shuffle 的构造直接暴露给 MLLM，模型可能根据文本模式猜答案而不是看视频。pairwise prompt 应随机左右顺序，并要求先描述可见动作再选择。
6. **evaluator leakage**：如果 sidecar 参与挑样、prompt tuning 或 reward 设计，就不能再作为同一主表 claim 的最终 evaluator。

## 7. 最小可执行 Pilot

样本：

1. 使用已有 observation pool：`64` 条 HumanML3D-E test split `>=3 events` 样本。
2. pilot v0 只取 `12` 条：固定 seed `004965 / 008463 / 001969 / 003245`，再从 `5plus` 高风险 bucket 取 `8` 条。
3. 每条先跑 `full / drop / shuffle`，replace 只抽 `4` 条 sanity case，避免一开始被细粒度语义拖死。

输入产物：

1. `render.mp4`
2. `grid.jpg`
3. `events.json`
4. `condition_meta.json`
5. `prompt.txt`

输出字段：

```yaml
sample_id: "004965"
condition: "shuffle"
input_type: "grid+video"
provider: "gpt-4o"
model_version: "record_exact_api_model"
prompt_hash: "sha256"
render_hash: "sha256"
visible_events: [0, 1, 2]
missing_events: []
unclear_events: [3]
observed_order: [0, 2, 1, 3]
pairwise_choice: "original_order"
confidence: 0.57
freeform_rationale: "short paraphrase only"
route_decision: "human_review"
leakage_flag: false
```

通过标准：

1. 在 `12` 条 pilot 中，MLLM 输出 JSON parse 成功率 `>= 95%`。
2. 人工快速复核中，明显可见事件的 presence 判断大体一致；目标不是高精度，而是证明不是随机回答。
3. 对 `drop`，被 drop 的 event 在视频中明显不可见的 case 能被标为 missing / unclear。
4. 对 `shuffle`，至少能在人工可读的 case 上给出非随机的 observed order。
5. sidecar 的 high-risk route 能提高人工复核命中率，而不是把所有样本都标成 uncertain。

停止标准：

1. skeleton render 人工都难以读懂，先停 sidecar，修 render。
2. MLLM 对 skeleton 输出大量幻觉，且 grid/video 两种输入都无法缓解。
3. full/drop/shuffle 的回答与人工复核接近随机。
4. 成本或延迟超过开发期可承受范围。
5. 任何人试图把 sidecar verdict 写进 formal final evaluator 或 main-table judge，立即降级为 qualitative case study。

## 8. 防止 Evaluator Leakage 的硬边界

1. Sidecar 只服务 generation-side diagnostic、evaluator routing、human-review prioritization。
2. Sidecar 不进入 reward scorer、formal judge、final evaluator、main-table metric。
3. 如果某个 MLLM sidecar 输出被用于筛选样本、调 prompt、调 guidance 或挑 case，它就不能再评价同一批结果的最终提升。
4. 若未来想把 MLLM judge 升级为 paper metric，必须另开 human calibration：固定 blind protocol、held-out sample、多人标注、一致性统计，并与 TMR / ChronAccRet / Event-T2M self eval 分离。
5. MotionPatches 仍不进入正式 eval / scorer / judge / reward 链路；本 note 不改变该边界。

## 9. 建议

可行但只适合作为 Plan B sidecar。推荐执行顺序是：

1. 先用已有 HumanML3D-E observation pool 做 `12` 条 render sanity。
2. 先跑 grid，再跑少量 video；优先验证 MLLM 是否能读 skeleton。
3. 只记录结构化 side evidence 和 route decision。
4. 若 pilot 通过，再扩到 `64 x full/drop/shuffle` 的离线诊断。
5. 在任何版本中都不要把 MLLM sidecar 写成 formal final evaluator，除非之后完成独立人类校准。
