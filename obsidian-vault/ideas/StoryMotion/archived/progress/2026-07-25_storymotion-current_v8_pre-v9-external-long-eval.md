---
title: "StoryMotion Current v8 before v9 external long evaluation"
status: archived
hypothesis: |
  C3-25 seed17 105K remains the audited Unified mainline, but single-Human
  generation quality remains the P0 blocker. The native Camera-free Stage1,
  Human128 Stage2 topology, GestureLSM system-control, and DanceCamera3D
  Camera-completion screens all stopped. No capacity-ceiling or new joint claim
  is authorized.
tags:
  - StoryMotion
  - version
  - stage1
  - stage2
  - human-first
  - status/archived
aliases:
  - StoryMotion-v8-pre-v9-external-long-eval
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
archived_predecessor: "[[archived/progress/2026-07-24_storymotion-current_pre-human-first-orthogonalization]]"
created: 2026-07-12T14:30:00+08:00
refactored: 2026-07-24
updated: 2026-07-25
archived: 2026-07-25
superseded_by: "[[current]]"
---

# StoryMotion Current v8 before v9 external long evaluation

> [!warning] 已归档
> 本页冻结 2026-07-25 三个 `105K` 外部/匹配臂正式评估前的 v8 决策面。当前结论见 [[current]]；本页旧的“无长训/E3 未实现”文字只保留时间点 provenance。

> [!abstract] 当前裁决
> v8.1C C3-25 seed17 `105K` 仍是 Stage1/Stage2 Unified mainline。P0-H128-S2、E1 G-SYS-H 与 E2 D-SYS-C 均已按各自 screen gate 停止；没有长训授权，也没有证据把问题单独归因为参数容量或已证明的 Stage2 backbone 能力上限。E3/E4 没有获准实现或训练；既有 E4 草稿骨架保持隔离且不构成 evidence。

## 1. 当前决策板

| item | current state | decision |
| --- | --- | --- |
| Unified mainline | C3-25 seed17 `105K` | 保持；Human-only specialist 的失败不替换 mainline |
| P0 blocker | single-Human semantic/distribution、pose 与 heading 不能同时过门 | Human-first |
| Human-only native mixed view | closed；不形成 Pareto win | 不做 pure4,053 formal，不晋升 specialist |
| no-update attribution | task-row、Camera context、objective/manifold、heading 与 architecture path 已闭合 | 旧 run 不是真正 Human-only；后续轴必须使用独立 contract |
| P0-HVIEW-1 | superseded before launch | `192D` 内置零 Camera 仍不能回答 true Human-only topology |
| P0-H128-S2 | fresh r2 的 30K/35,006 N=512 screen 已停止 | fixed-C3 Human-only topology 未过 semantic、geometry 与 physical hard gate；不续 105K |
| P0-H128-S1 | short r2 已关闭；pure4,053 无 Pareto win | 停止；不做 full-budget、不构建 cache、不接 Stage2 |
| E1 G-SYS-H | Stage1 part floors 可审计；Stage2 5K N=512 已停止 | full-system Human control；semantic/coverage broad regression，不续长训 |
| E2 D-SYS-C | original、bounded-FOV 与 no-framing screens 均停止 | observed-Human Camera completion control；不得写成 joint generation |
| E3 / E4 matched-backbone | deferred；无获准 optimizer；既有 E4 草稿隔离 | 按用户约定，成功长训后先提交详细 pipeline 修改方案与流程图，经确认后才落实 |
| joint / Unified / VACE | paused | Human hard gate 通过后才重开 |

## 2. 最新证据与决策

### 2.1 Human-only loss 语义

`human_loss_human_branch` 是实际训练的 task ID 1 / Direct-H 目标：`[H_t,C_t] + [0,e_H]`，只监督 Human branch。它的 test curve 在约 `33K` 后恶化，是当前更直接的 late-overfit 信号。

`human_text_loss_human_branch` 是未训练的 task ID 3 Camera-free transfer probe：近似 `[H_t,0] + [0,e_H]`。Human-only 对该 task 的概率为零，row 3 没有训练更新；它不能作为主训练目标或 checkpoint-selection metric。

因此当前准确表述是：Human-only 在未训练的 Camera-free transfer task 上具有最差的最终绝对 loss；主任务 overfit 的证据来自 active Direct-H test curve，而不是仅凭 inactive transfer loss。精确曲线点只见 [[StoryMotion-valid-metric-ledger]]。

### 2.2 根因裁决

- 旧 Human-only 只证明在原 Unified `192D` topology 内移除 Camera/joint updates 无效；其未训练 task row 3、paired Camera context 与自由 Camera state 是独立混淆。
- 实现与 no-update 证据排除了 latent LayerNorm 稀释、Human loss 被 `192D` mean 缩小、attention sink、大块 Camera 参数占用，以及 Human-only 特有自由 Camera feedback作为主要解释。
- Stage1 Human target 存在弱 Camera coupling，`t=799` heading amplification 获得支持；当前 manifold projection 与稳定负 shared-gradient conflict 未获支持。
- fresh Camera-free Stage1 short 的 recon/velocity component loss 略低；decoded geometry 的 aggregate point estimates 没有一项改善，paired uncertainty 中只有 heading 退化稳定非零。因而“删掉 Camera representation surface 足以修复 Human”被否定，objective–decoded-heading 局部错位获得支持。该 system screen 不能细分 input dim、encoder coupling或 decoder reinitialization 的单项因果。

完整输入、数值、置信边界与 artifact identity 只见 [[StoryMotion-valid-metric-ledger]]；因果协议与限制见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。

### 2.3 当前 architecture / external-control 裁决

P0-H128-S2 已在 30K 与 35,006 的 N=512 screen 停止。E1 的 part-wise tokenizer reconstruction floor 可以建立 Stage1 floor，但其 Stage2 system control 在 decoded Human semantic/coverage 与 latent-to-decoded agreement 上失败；E2 的两个 framing repair 虽有局部 Camera 几何恢复，仍在 CLaTr、out-of-frame 与固定样本视觉上失败。E1 是 tokenizer、objective、condition 与 backbone 的完整系统 control；E2 只测试 observed-Human Camera completion。

因此在该历史时间点没有 E1/E2 长训，也未触发 E3/E4 的实现阶段。四臂 interface、变量矩阵、stop/continue contract 与 observability 条款现归档于 [[archived/experiments/2026-07-25_storymotion-v9-external-system-backbone-adaptation-closed]]；数字与 immutable identity 只见 [[StoryMotion-valid-metric-ledger]]。

## 3. 三个直接动作

1. **P0-HCTX-1 / P0-HARCH-0 / P0-HCAM-S2 — complete：** task row、Stage1 coupling、Stage2 Camera-state feedback与 LayerNorm/容量替代解释已分开；Camera feedback 未形成 Pareto repair。
2. **P0-MAN-1 / P0-HDG-1 — complete：** objective、decoder/manifold、shared-gradient 与 `t=799` heading oracle 已闭合；projection arm 被排除。
3. **P0-H128-S1 / S2 与 E1/E2 — stopped：** 四条相互独立的 screen 均未过各自 gate；不续长训、不替换 C3-25 mainline，也不据此实现 joint-only extension。

## 4. Human hard gate

最终 single-Human generator 必须同时满足：

- FDTMR、TMR 与 HCov 相对 Parent 不出现 broad regression；
- root-aligned pose、heading、global/root trajectory 形成 Pareto 改善或严格非劣；
- 固定样本视觉质检通过；
- blind/no-reference Human physical-quality 质检通过；
- latent test loss 与 decoded generation quality 方向一致。

Stage1 reconstruction screen 本身不能通过本生成 gate。任一生成条件失败就停止对应 continuation。screen 通过也不自动授权 joint/Unified/VACE；恢复这些训练还要求同一 frozen Human source 可被 Camera 分支可靠消费，且 joint parallel 不回退。

## 5. 当前边界

- 所有 StoryMotion Stage1/Stage2 tokenizer 必须满足 `is_causal is False`。
- C3-25 `105K` 当前 formal evidence 与 run identity 不回写、不替换。
- 当前没有由本轴授权的 StoryMotion 训练/评估进程；5090 GPU2 与两个 4090 slot 均已从 E1/E2/P0 screen 释放。
- 任一未来 E1–E4 optimizer run 必须启用 run-local TensorBoard，并至少在总进度 `20%/40%/60%/80%/100%` 保存 checkpoint；缺任一合同字段时在 optimizer 构造前停止。
- 数据清洗保持 versioned、reversible、pair-level quarantine；完整合同只见 curation owner。
- root-aligned MPJPE 只移除 root translation，不移除 heading；不得称为 local-pose error。

## 6. Canonical owners

- 数值、screen/formal evidence、hash、artifact registry、uncertainty：[[StoryMotion-valid-metric-ledger]]
- open causal question、预注册变量与 stop/continue gate：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]
- version-family 命名、完成事件与 invalidation：[[version_family]]
- metric/evaluator/decoder I/O 定义：[[StoryMotion-metric-computation-io]]
- reliability 与论文级外推边界：[[StoryMotion-iclr-reliability]]
- v8.2333 cleaning、manifest lineage 与 curation gate：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]
