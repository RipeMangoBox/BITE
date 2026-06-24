---
title: "Original100 模型-样本能力整理（a3）"
created: 2026-05-27T00:00:00+08:00
updated: 2026-05-27T00:00:00+08:00
type: diagnostic_summary
status: complete
tags:
  - MoDebug
  - Original100
  - model-diagnosis
  - sample-analysis
role: diagnostic
used_for:
  - failure_family_selection
  - trace_hypothesis_prep
limitations: |
  Original100 仅为 100 条 diagnostic samples，不是 benchmark，也不是 final evaluator。
  本文遵循用户先验：description 非空即记为问题；GT 少数样本存在左右/视角或文案噪声；本集脚步滑动/物理失真较少，更多体现为指令跟随不足。
source_files:
  - obsidian-vault/paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/eval/original100_posthoc_20260527/annotation_joined.jsonl
  - obsidian-vault/paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/eval/original100_posthoc_20260527/per_prompt_problem_matrix.tsv
  - obsidian-vault/paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/inputs/hml_original100_sample_manifest.tsv
---

## 结论摘要

- 100 个 Original100 diagnostic samples 中，4 模型全对 `61` 个，全错 `3` 个，部分模型能做对 `36` 个。
- 模型问题数为：`MoLingo 12 < MotionGPT 14 < MoGenTS 21 < MoMask original 23`。这里是本诊断集上的 failure count，不代表最终排序。
- GT 自身有问题 `6/100`，主要是左右肢体/视角歧义或速度词不准：hml_orig100_test_007__full, hml_orig100_test_009__full, hml_orig100_train_031__full, hml_orig100_train_033__full, hml_orig100_train_035__full, hml_orig100_train_062__full。剔除这些样本后，侧别相关难点并没有减弱。
- 这 100 个样本里，主导问题不是脚步滑动或明显物理失真，而是指令跟随不足，尤其是侧别 grounding、阶段覆盖和轨迹语义保持。

## 1. 都能做好的 sample 有什么特点？

- 共性是约束稀疏：短文本、短到中等长度动作、单阶段或弱阶段切换、少侧别、少非对称上肢角色。
- 最稳定的两个主类是 `sit_squat_posture` 与 `direction_turn`，各有 `8/10` 个 sample 被四模型同时做对；`upper_body_gesture` 也有 `7/10` 个全对。
- 短文本优势很强：`<=8` 词样本共 `30` 个，其中 `26` 个四模型全对，平均每样本失败数仅 `0.2`；而 `>=16` 词样本只有 `14/35` 全对。
- 生成路径上的共性可以保守表述为：当文本只要求一个主导动作原语，且不要求长期维护左右/阶段/轨迹等稀疏约束时，四个模型都能沿着强动作先验生成出可接受结果。这里更像“单主导语义不被冲散”，而不是更细粒度的 token-level 成功。
- 代表 sample 可见全对集合中大量简单前进、单次转向、坐下/站起、单一上肢动作。

## 2. 都做不好的 sample 有什么特点？

- 四模型全错只有 `3` 个，但这 3 个足够集中地暴露了 hardest corner cases：
  - `hml_orig100_test_003__full`: `a person stands normally then begins hops on their right foot while their left foot is elevated then stops and stands normally.`
  - `hml_orig100_test_020__full`: `a man slowly raises both arms high over his head in a stretch, holding the posture for several seconds, with his right arm stretched out to his side.`
  - `hml_orig100_train_050__full`: `a man turns to the left and reaches up to grab something with his left hands.`
- 这 3 个 sample 的共性不是“动作复杂”本身，而是同时要求多个稀疏约束：
  - 侧别或非对称角色明确：如右脚 hop、右臂抬高但另一只手外展、左转同时左手抓取。
  - 阶段切换或停止/持姿存在：如 `test_003` 的 hop 后停住，`test_020` 的 raise-hold-non-symmetric arm。
  - 局部肢体角色和全身路径/姿态同时被指定。
- 交互统计支持这一点：
  - 仅含侧别词的样本：`49` 个，平均失败数 `1.204`。
  - `left/right + sequential`：`22` 个，平均失败数升到 `1.636`。
  - `left/right + sequential + long_text`：`19` 个，平均失败数 `1.737`，只有 `4/19` 个四模型全对。
  - `left/right + sequential + hold/stop`：`11` 个，平均失败数 `1.727`。
- 需要强调一个反例：`left/right + object` 子集的平均失败数只有 `0.842`。这说明“侧别词”并非在任何上下文都同样困难；真正高风险的是它与多阶段、长文本、停止/持姿叠加时的复合负担。

## 3. 部分能做好的 sample 有什么特点？哪些模型在哪些类型上更稳/更弱？

- `36` 个 partial samples 是最有信息量的部分，因为它们把 sample 难度和模型路径差异分开了。最大的 partial pattern 簇是：
  - `1100`（MotionGPT + MoLingo 对，MoMask + MoGenTS 错）有 `7` 个。
  - `1110`（前三者对，仅 MoGenTS 错）有 `5` 个。
  - `0111`（仅 MotionGPT 错）有 `4` 个。
  - `1000`（仅 MotionGPT 对）有 `2` 个：`train_002`、`train_006`。
  - `0100`（仅 MoLingo 对）有 `2` 个：`test_002`、`test_013`。
- 这说明前两者整体更稳，但各自的强项不完全相同。

### MotionGPT

- 可稳写的个性：错误更集中，而不是四处都掉。粗主题里 `left_right_grounding` 占其主题命中的 `45.5%`，远高于 stage/trajectory。
- 在本诊断集中，它在轨迹关键词子集上相对稳定：`19` 个 trajectory 关键词样本里错 `3` 个；若去掉仅 spin 的样本，在 `16` 个 circle/8字/jagged/curve/bend/arc/zigzag 样本里错 `2` 个。
- 但不要写成“轨迹能力更强”这种全局结论。更稳妥的表述是：在这组轨迹语义样本里，MotionGPT 的错误少于 MoMask 和 MoGenTS，并与 MoLingo 接近。
- 代表 case：`hml_orig100_train_002__full` 只有 MotionGPT 正确完成 tight circle + facing constraint；`hml_orig100_train_006__full` 只有 MotionGPT 正确完成右手拿布、左手举物、再擦拭。

### MoLingo

- 总体问题数最低（`12`），且在侧别和非对称上肢上相对最稳。
- `left/right + upper_body` 子集 `37` 个样本中，MoLingo 错 `7` 个，低于 MotionGPT `9`、MoMask `13`、MoGenTS `14`。若去掉多阶段，仅看 `left/right + upper_body + 非 sequential` 的 `20` 个样本，MoLingo 只错 `2` 个，是四者最低。
- 因此可以稳写：MoLingo 在“非对称上肢侧别”上相对最稳，但在 `dance_exercise`、部分对象交互和阶段覆盖上仍会掉。
- 代表 case：`hml_orig100_test_002__full` 与 `hml_orig100_test_013__full` 体现了它在左右手非对称和复杂阶段拼接上的优势。

### MoMask original

- 它不是只在一个点上差，而是多点一起掉：总问题数最高（`23`），左右侧别、轨迹形状、阶段覆盖都明显受损。
- 粗主题里 `left_right_grounding 40%`、`trajectory_shape 16.7%`、`stage_coverage 13.3%`。
- 相对更稳的是 `upper_body_gesture` 主类（`10` 个样本中 `0` 错）和对象交互子集，但一旦叠加侧别、计数/速度、长文本，退化明显。

### MoGenTS

- 整体略好于 MoMask，但脆弱面相似：总问题数 `21`，侧别、阶段覆盖、轨迹语义都较弱。
- 在 `left/right + upper_body` 子集里最差（`14/37` 错；非 sequential 子集 `8/20` 错）。
- 在 trajectory 关键词子集上也偏弱：`19` 个样本错 `7`，`16` 个非 spin-only 样本错 `6`。
- 可稳写的说法是：MoGenTS 更容易在非对称上肢与阶段/轨迹约束叠加时失稳。

## 4. 后续最值得落地的显著指标与可视过程/结果建议

- 最小可执行指标集只保留两个主指标，另外三类内容更适合作为可视化或子分析。

### P0 指标

1. `LRGA`（Left/Right Grounding Accuracy，左右/侧别 grounding 准确率）
   - 目标失败：左/右肢体、左/右转、顺时针/逆时针跟随错误。
   - 输入：含侧别描述的样本、模型视频或骨架、人工侧别判定表。
   - 计算：在 `49` 个侧别样本上逐模型判定是否满足文本指定侧别；必要时再拆上肢/下肢/全身旋转子分数。
   - 预期信号：MoLingo 最稳；MotionGPT 的总错误较少但更多集中在该项；MoMask 与 MoGenTS 更差。
2. `SCS`（Stage Coverage Score，动作阶段覆盖分数）
   - 目标失败：漏做后半段、只做前半段、停得过早、阶段拼接断裂。
   - 输入：显式多阶段文本、阶段分解表、模型视频或骨架时间轴。
   - 计算：对每个多阶段样本计算“被识别出的阶段数 / 文本总阶段数”；主版本先不要求顺序，严格版可另查顺序。
   - 预期信号：在 `left/right + multi-stage + long_text` 子集上区分度最大。

### 更适合做可视化或子分析

- 根轨迹语义叠加图：支持 circle/8字/jagged/curve 这类 case，但样本只有 `16-19` 个，更适合定性展示，不宜作为主指标。
- 阶段-时间对齐条形图：非常适合解释 `train_006`、`test_013`、`test_020` 这类“前半对、后半丢”的样本。
- 左右肢体高亮关键帧对比：直接支撑 LRGA，适合展示 `train_006`、`test_013`、`train_050`。
- `Upper-limb LRGA` 可以保留为 LRGA 的子分析，不需要独立升级成第三个主指标。

## 风险声明

- `Original100` 是 diagnostic sample set，不是 benchmark，也不是 final evaluator；不能拿这里的 `12/14/21/23` 问题数做最终模型排序。
- train-source 样本与 GT 噪声同时存在，结论只说明“在这 100 个样本上的行为模式”，不能直接外推成 held-out generalization。
- `GT 6/100` 的左右/视角/速度噪声必须单列；它们不改变“侧别是主要难点”的趋势，但会影响个别样本的责任归因。
- 轨迹相关结论基于 `16-19` 个样本，左右+上肢子集基于 `37` 个样本，统计力度低于侧别总体结论。
- 本文不把脚步滑动/物理失真当主结论；在这批样本里它只是一类次要现象。

## 证据样本

- 四模型全错：`test_003`, `test_020`, `train_050`。
- 仅 MotionGPT 对：`train_002`, `train_006`。
- 仅 MoLingo 对：`test_002`, `test_013`。
- MotionGPT + MoLingo 对、后两者错 的最大 partial 簇有 `7` 个，说明前两者在相当一部分复合约束样本上更稳。
