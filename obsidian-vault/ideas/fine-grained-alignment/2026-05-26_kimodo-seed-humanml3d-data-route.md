---

## title: "Kimodo/SEED 与 HumanML3D 双轨数据路线"

created: 2026-05-26T00:00:00+08:00
updated: 2026-05-26T00:00:00+08:00
status: active
hypothesis: "MLPA 和 MoDebug 的数据路线应从 VLM 自建 HumanML3D event ground truth 转向 Kimodo/SEED 的官方 timeline 标注；HumanML3D/HumanML3D-E 只保留为快速 baseline、诊断和伪标签工作台。"
tags:

- MLPA
- data_route
- Kimodo
- SEED
- HumanML3D
- Qwen_VL
- MoDebug
source_papers:
- "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]"
- "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]"
related_notes:
- "[[ideas/fine-grained-alignment/README|MLPA README]]"
- "[[ideas/fine-grained-alignment/roadmap|MLPA 当前路线图]]"
- "[[gates|MLPA 实验关口]]"

# Kimodo/SEED 与 HumanML3D 双轨数据路线

> [!abstract] 结论
> 第一阶段不再把 Qwen3-VL-Plus 对 HumanML3D 视频的 event captioning / grounding 当作可靠监督来源。主数据路线切到 Kimodo / BONES-SEED / SEED-Timeline，因为它公开提供 motion timeline event segment 与文本描述。HumanML3D/HumanML3D-E 仍保留，但角色降级为 baseline-rich 的快速诊断、failure bank 和伪标签流程验证。

## 1. 总体决策

当前应采用双轨路线：

1. **Kimodo/SEED 主线**：服务 MLPA 的 event-time correspondence、timestamping、rerank、verifier 和 MoDebug 的 event-level 快速实验。它是唯一已核到的、公开且较系统的 motion event segment 与 text event 对齐来源。
2. **HumanML3D/HumanML3D-E 支线**：服务快速 baseline、训练体量小的 ablation、renderer / feature / prompt 流程调试，以及 MoDebug failure bank。它不能承载 event boundary ground truth 或 final evaluator。

切换原因不是 HumanML3D baseline 不重要，而是用户已测的两种 VLM 自建流程都不稳定：

1. Qwen3-VL-Plus 直接看完整 HumanML3D video 做 event grounding captioning：event 划分过细或过粗，caption 过复杂。
2. 提供 HumanML3D-E event decomposition 后，让 Qwen3-VL 看完整 video 做 motion event grounding：时间定位不准。

这说明完整视频一次性 `event discovery + caption + grounding` 是欠约束任务。即使 Qwen3-VL 有一定视觉能力，也不应把它升级为 motion event ground truth 生产器。

## 2. 官方 Kimodo / SEED 资源层级


| 资源                                   | 类型                           | 能提供什么                                                                                                  | 不能提供什么                                      |
| ------------------------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| `bones-studio/seed`                  | BONES-SEED motion 数据本体       | SOMA uniform / proportional BVH、Unitree G1 CSV、shape assets、metadata                                   | 不是 HumanML3D 263/272D；不是公开 SMPL-X event 数据集 |
| `nvidia/SEED-Timeline-Annotations`   | timeline 文本标注                | `filename`、`overview_description`、`events[start_time,end_time,description]`、`propagated_from_filename` | 不含 motion 文件；部分 event 是自动传播                 |
| `nvidia/Kimodo-Motion-Gen-Benchmark` | benchmark metadata 与官方 split | BONES-SEED / SOMA 官方 train/test split、text2motion / constraint test cases、Kimodo benchmark prompts     | 不是小规模训练集；不是 SMPL-X 数据集                      |
| `nvidia/Kimodo-SMPLX-RP-v1`          | model repo                   | SMPLX-body skeleton 的 Kimodo model weights / stats                                                     | 不是公开 SMPL-X motion-text-event 数据集           |


官方链接：

- [SEED-Timeline-Annotations](https://huggingface.co/datasets/nvidia/SEED-Timeline-Annotations)
- [Kimodo-Motion-Gen-Benchmark](https://huggingface.co/datasets/nvidia/Kimodo-Motion-Gen-Benchmark)
- [Kimodo-v1 collection](https://huggingface.co/collections/nvidia/kimodo-v1)
- [BONES-SEED](https://huggingface.co/datasets/bones-studio/seed)
- [Kimodo-SMPLX-RP-v1](https://huggingface.co/nvidia/Kimodo-SMPLX-RP-v1)

已核事实：

1. SEED-Timeline 官方标注约 `142,220` labeled motions、`352,703` timeline segments，平均 `2.48` segments / motion。
2. Kimodo benchmark 官方 split 行数为 `train=128,351`、`test_content=7,017`、`test_repetition=6,888`。
3. 没有发现官方小规模、已切分、event-aligned 的 SMPL-X 或 SMPL-X-like 数据集。
4. 若为了可信度，需要优先使用 Kimodo benchmark 的官方 split；如果必须先做小规模调试，只能从 official train split 生成 disposable cache，且不得进入 final evaluation。

## 3. HumanML3D / PoseFix / Qwen3-VL 支线修正

HumanML3D 仍值得保留，因为 baseline 丰富、训练体量小、工程反馈快。但不能再采用 full-video free-form 操作。

失败根因拆分：

1. **模型局限**：skeleton video 缺少自然图像语境，root trajectory、facing、foot contact、step count 对 VLM 不显式；完整视频压缩后更难稳定定位细边界。
2. **流程欠约束**：一次性要求模型完成事件发现、命名、时间定位和计数判断，缺少候选窗口、几何先验、order constraint 与二次验证。
3. **数据标签边界**：HumanML3D caption 不是严格 temporal event label；HumanML3D-E event decomposition 是文本事件清单，不等价于 motion-side boundary ground truth。

优先替代 pipeline 应改为 FineMotion/PoseFix-style，而不是继续让 Qwen 做完整视频自由 caption：

```text
HumanML3D / HumanML3D-E motion
-> fixed 0.5s snippets
-> first / last 22-joint pose pair, root-centered
-> PoseFix modifier
-> root trajectory / yaw / contact / velocity metrics
-> snippet evidence record
```

角色边界：

1. PoseFix 描述的是 pose-pair articulation delta，不是动态 event caption。
2. root trajectory、yaw、contact、velocity 必须作为独立 motion-side evidence 记录。
3. 该路线适合作为 weak body-part sidecar、MLPA body cue diagnostic 和 MoLingo phrase-anchor side signal。
4. 该路线不能提供正式 motion event boundary GT 或 final evaluator。

如果仍尝试 Qwen，应将其降级为窗口级 verifier，而不是数据生产器：

```text
HumanML3D / HumanML3D-E text events
-> geometry change-point candidates
-> short-window VLM yes/no verification
-> multi-scale / multi-view consistency
-> DP or Viterbi ordered alignment
-> pseudo boundary + confidence + unstable flag
```

操作细节：

1. 不再让 Qwen 看完整 video 做自由 caption；必要时切 `1.5-2.0s` 窗口，stride `0.5s`，另加 `3-4s` 粗窗口。
2. 每个窗口提供 skeleton video、timestamp contact sheet、top-down root trajectory、facing arrow、foot-contact strip。
3. 对 HumanML3D-E，输入 ordered event candidates，让 Qwen 只做窗口级 `visible / partial / no / ambiguous` 与 `score=0-3`。
4. prompt 禁止改写 event、禁止生成新 event、禁止输出全局时间戳；只输出 JSON evidence flags。
5. 对 HumanML3D 无 event list 的情况，窗口 caption 限制为 `<=8 words` dominant action；除非有 trajectory/contact 证据，否则禁止 step count 和方向判断。
6. 用 root speed、yaw velocity、pelvis height、hand/foot velocity、foot contact 产生候选 change points。
7. 重打分采用 `VLM binary score + geometry score + text-event prior`，再用 DP / Viterbi 做 ordered alignment。
8. 输出 `core_start/core_end + transition_before/after + confidence + unstable flag`，不要只输出硬边界。

证据角色：


| 输出                              | 允许角色                             | 禁止角色                              |
| ------------------------------- | -------------------------------- | --------------------------------- |
| Qwen window yes/no score        | diagnostic / pseudo-label        | final evaluator                   |
| Qwen timestamp / boundary       | pseudo-label                     | ground truth                      |
| HumanML3D-E event decomposition | text-side event candidate        | motion-side timestamp supervision |
| geometry change point           | candidate proposal / side signal | semantic event label              |
| DP / Viterbi alignment          | diagnostic alignment             | held-out final evidence           |


退出条件：

1. 若主 claim 需要精确 temporal grounding、span-supervised training 或 event completion 定量指标，切到 Kimodo/SEED。
2. 若窗口化后边界漂移仍大于 `0.5-1.0s`，或多视角 / 多尺度一致性低，HumanML3D 只保留为 failure bank。
3. 若论文主表需要 held-out final evaluator，HumanML3D/Qwen 输出不得进入主表。

## 4. 对 MLPA / MoDebug 的执行顺序

推荐顺序：

1. 直接用 Kimodo/SEED 官方 timeline 与官方 split 跑 MLPA event-to-window pipeline smoke，目标是打通 data loader、window proposal、correspondence record、null / ambiguity。
2. 同时保留 HumanML3D/HumanML3D-E 的窗口化 Qwen pipeline，用于 baseline-rich 的小样本 diagnostic，不进入主 claim。
3. 若需要小规模加速，只从 Kimodo official train split 建 disposable cache；评估使用 `test_content_split_paths.txt` 与 `test_repetition_split_paths.txt`。
4. 优先训练 lightweight aligner / verifier / reranker；暂不 full generator retrain。
5. 只有 timestamping 与 rerank gate 通过后，才尝试 generator-side scaffold 或 MoLingo / MoMask / EventT2M 类 backbone coupling。

最小下一步：

```text
SEED-Timeline JSONL + Kimodo official split
-> join filename with BONES-SEED / SOMA motion path
-> convert start_time/end_time to 20fps frame windows
-> load SOMA motion or validated feature cache
-> window-level event correspondence scoring
-> compare equal split / full-caption scorer / Qwen window verifier
```

## 5. Reviewer 风险与修补


| 风险                                                | 严重程度 | 修补                                                                                           |
| ------------------------------------------------- | ---- | -------------------------------------------------------------------------------------------- |
| 把 Qwen / VLM output 当 event ground truth          | 高    | 只标记为 pseudo-label / diagnostic / side signal                                                 |
| 用 HumanML3D evaluator 评价 SOMA-trained model 并做主结论 | 高    | 只作 cross-check；主结论在同一数据生态内评估                                                                 |
| SOMA77 -> HumanML3D22 映射未充分验证                     | 中高   | first-stage 尽量用 event-time correspondence，不把映射质量写成贡献；补可视化和 finite/loader/retarget provenance |
| 非官方小数据削弱可信度                                       | 中高   | 不自建 benchmark；最小调试 cache 必须来自 official train split 且不参与 final eval                           |


## 6. 记录可靠性

- date: `2026-05-26`
- artifact_path: `paperIDEAs/fine-grained-alignment/2026-05-26_kimodo-seed-humanml3d-data-route.md`
- evaluator: `Codex + Hegel subagent + DeepSeek cross-check`
- protocol: `official HF README/API audit; HumanML3D/Qwen failure-route review`
- motion_source: `BONES-SEED/SOMA uniform; HumanML3D/HumanML3D-E for diagnostic only`
- condition_pair: `use Kimodo/SEED official split; HumanML3D VLM pseudo-label route -> diagnostic only`
- n/evaluable: `SEED timeline 142220 motions / 352703 segments official; Kimodo official split train=128351, test_content=7017, test_repetition=6888`
- coverage: `data route selection, official split availability, HumanML3D/Qwen diagnostic pipeline, single-4090 batch-size boundary`
- role: `diagnostic`
- used_for: `selection`
- limitations: `未下载全量 Kimodo official benchmark 到本地；未重新跑训练；HumanML3D/Qwen 改进 pipeline 尚未做实测，只作为下一步 gate 设计。`

