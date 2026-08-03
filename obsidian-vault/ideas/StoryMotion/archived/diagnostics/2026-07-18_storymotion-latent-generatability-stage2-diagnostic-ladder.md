---
title: "StoryMotion Human-first Diagnostic Ladder"
status: v9_e5_e6_human_controls_closed
archived: 2026-08-03
hypothesis: |
  Human128 and the fixed-C3 external Human-system diagnostics are closed.
  E5 MARDM and E6 ViMoGen-light establish Human free-generation capability
  but do not close the strict physical gate or isolate a pure backbone effect.
  These historical controls do not replace the v11 C0-LAT/C0-GEO co-mainline;
  any reopened joint-first work remains owned by its dedicated design page.
tags:
  - StoryMotion
  - stage1
  - stage2
  - human-first
  - diagnostic
  - latent-diffusion
  - root-cause
aliases:
  - StoryMotion-Latent-Generatability-Ladder
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
archived_predecessor: "[[archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder_closed-through-human-only_20260724]]"
created: 2026-07-18T14:44:45+08:00
refactored: 2026-07-24
updated: 2026-07-28T12:19:45+08:00
---

# StoryMotion Human-first Diagnostic Ladder

> [!abstract] 当前用途
> 本页拥有 single-Human 与 matched-backbone 因果问题、预注册输入和 stop/continue gate。v9 当前裁决由 [[current]] 拥有；正式与 screen 数字由 [[StoryMotion-valid-metric-ledger]] 拥有，hash 与 artifact registry 由 [[Storymotion-exp-sha]] 拥有；完成时间线与 invalidation 由 [[version_family]] 拥有。

## 1. 固定边界

- 当前system mainline是v11 C0-LAT／C0-GEO `105K`；本页的历史Human-only specialist失败不改变该selection，C3-25保留former-mainline baseline。
- single-Human specialist 未通过 hard gate，因此不得替换 Unified mainline。另行预注册的 joint-first dual-expert 路线由 [[2026-07-25_storymotion-gesture-dc3d-joint-dual-expert-design]] 独立授权，不把 Human-only 结果外推为 joint 能力。
- no-update attribution 已完成。P0-H128-S2 保持 fixed C3 representation；用户另行显式授权的 P0-H128-S1 独立 Stage1 system screen 已按 short gate 停止。两者不共享 checkpoint、optimizer、cache 或结论，不构成 factorial comparison。
- 所有 Stage1/Stage2 tokenizer 必须满足 `is_causal is False`。
- no-update 输出是 teacher-forced diagnostic，不是 DDIM50 自由生成或 formal promotion evidence。
- 已完成的 E1、E2、E3 eval 分别独占 4090 GPU0、4090 GPU1 与 5090 物理 GPU2；三路结束后均释放。未来任务继续遵守每个物理槽最多一个 StoryMotion train/eval process。

## 2. 已固定的语义事实

Human-only native run 仍是 `192D = Human128 + Camera64` 的 Unified 网络，并不是真正无 Camera 通道的 `128D` Human architecture。

实际训练 task 与未训练 transfer probe 必须分开：

- task ID 1 / Direct-H：输入视图为 `[H_t,C_t] + [0,e_H]`，训练更新只作用于 Human branch；这是 native Human-only run 实际训练的 task。
- task ID 3 / Human-text transfer：近似 `[H_t,0] + [0,e_H]`。Human-only run 对该 task 的概率为零，task row 3 未获更新，因此它只能是 Camera-free transfer diagnostic。

准确结论是：未训练的 Camera-free transfer task 不能代表主任务，optimizer 过程也不能替代 decoded generation 评价。stop/continue 只使用冻结 checkpoint 的 canonical Human metrics、decoded geometry/kinematics 与视觉证据。

## 3. Closed no-update attribution index

下列 causal questions 已闭合，不再占用 live ladder。数值与置信边界只见 [[StoryMotion-valid-metric-ledger]]；固定输入、执行协议路径与 hashes 只见 [[Storymotion-exp-sha]] 及对应 immutable run root。

| diagnostic | separated variable | closed result | downstream effect |
| --- | --- | --- | --- |
| P0-HCTX-1 | task row 1/3 × native/zero/shuffled Camera64 | 未训练 row 3 是独立混淆；row 1 下 teacher-forced Camera-context dependence 获得支持 | 进入 architecture-path attribution；不单独授权 row/view 混改 |
| P0-MAN-1 | raw prediction、Stage1 identity floor、`Enc(Dec(pred))` projection、decoder objectives | 当前 projection 与稳定负 shared-gradient conflict 未获支持 | 不选择 projection 或 objective-replacement arm |
| P0-HDG-1 | `t=799` 的 yaw/root/pose6d/RIFKE oracle replacement | heading 是强 decoded-geometry amplifier | 仅作归因；不与本轮 view arm 叠加 |
| P0-HARCH-0 | Stage1 native/zero/shuffled Camera、latent/text normalization path、legacy/pure topology | raw latent LayerNorm dilution与大块 Camera capacity占用被排除；旧实验不具备 true Human-only construct validity | P0-HVIEW-1 启动前被取代；只选择 fixed-representation Human128 Stage2 topology |
| targeted Stage1 Camera probe v2 | small perturbation、coherent reference Camera、length-matched shuffle、OOD zero Camera | C3 Human target 有可测 Camera coupling；small perturbation 很弱，zero Camera 显著夸大效应 | 支持用户另行授权的 P0-H128-S1 system screen；不把它与 S2 合并归因 |
| P0-HCAM-S2 | free、zero、matched `q(C_gt,t)`、shuffled generated Camera state | 两个 checkpoint 均有强 cross-channel co-adaptation；非 free 状态没有 Pareto repair，Parent 通常更敏感 | 排除 Human-only 特有 Camera feedback 作为主要根因；不选择 zero/mask inference arm |

## 4. 单变量 Human short arm 选择门

P0-HCTX-1、P0-MAN-1、P0-HDG-1、P0-HARCH-0 与 P0-HCAM-S2 的 immutable artifact 已闭合。Stage2 topology 与已关闭的 Stage1 representation-system screen 使用两个相互独立的 fresh `r2` contract；不得把两条解释成一个联合 intervention。

候选必须满足：

1. 至少一个主要机制由 paired、跨 timestep 证据支持，且不存在同等强度的替代解释。
2. 变化仅落在一个轴：true `128D` Camera-free architecture、train/inference view consistency、inference manifold projection、单一 decoder anchor，或 prediction objective。
3. 固定其余 cache、normalization、decoder、IDs、seed、budget、batch、sampler 与 evaluator。
4. 先在约 `30–35K` screen；未经 Human gate 不继续长训。

### 4.1 P0-H128-S2 Stage2 topology 短臂

| field | preregistered value |
| --- | --- |
| active run | `p0_c3_25_human128_stage2_topology_r2_0_35006_seed17_5090g2_20260724` |
| causal comparators | Human-only native matched `35,006` exposure boundary；Parent C3-105K Human hard gate |
| selected causal axis | legacy multi-surface Stage2 lacks true Human-only construct validity；free Camera feedback itself is not assumed causal |
| one changed axis | Stage2 topology contract：`192D/1024D` multi-surface → Human128 latent、Human512 text、single Human output |
| inherent removals inside that axis | no Camera input/text/output、no observation-mask channels、no task embedding；sampler never constructs a Camera tensor |
| unchanged Stage1 representation | C3-25 joint cache 的 native paired `E(H,C)` Human128 slice；明确标记 `camera_free_representation=false` |
| unchanged objective/model scale | START_X prediction target、Human full-cov normalization、width/depth、optimizer 与 LR schedule |
| unchanged exposure | fresh seed17；single Human task；每个 optimizer step 的 Human sample exposure 与 `[0,1,0,0]` native parent matched；batch 相同 |
| unchanged decode/eval | C3-25 owning Human decoder、ordered IDs、DDIM50、CFG、seed 与 evaluator |
| train boundary | fresh `0→35,006`；在 `30K` 与 `35,006` 保存 immutable screen snapshots |
| execution guard | fresh r2 已训练结束；30K 与 35,006 screen 均只占物理 GPU2，未并行启动第二个 StoryMotion train/eval |

`P0-HVIEW-1` 的旧 `mixed→isolated` 预注册在启动前标记为 `superseded_before_launch`。把 Camera64 置零但保留 `192D` input/output、task/text surfaces 和 joint Stage1 target 不能回答 true Human-only topology；其计划记录不删除，也不产生训练 artifact。

P0-H128-S2 把“true Stage2 Human-only topology”视为一个不可拆的 architecture axis。若它改善，结论只能是该整体 topology 修复有效，不能再把收益细分归因给 input dim、task embedding 或 text dim 中某一个子表面；objective、Stage1 与 decoder 仍保持固定。

首次同轴 run 在产生可续训 checkpoint 前触发安全停止，失败记录保留且 run root 不复用；fresh `r2` 从 step 0 开始。该 operational failure 不构成新的 causal arm。

### 4.2 P0-H128-S2 stop/continue screen

screen 使用与 Parent/Human-only learning curve 相同的 ordered N=512 IDs、seed17、DDIM50、CFG、owning decoder 与 evaluator，同时保留 fixed-sample 视频和 blind/no-reference Human physical-quality review。

- **stop**：任一 snapshot 的 FDTMR/TMR/HCov 继续 broad regression；或 RA pose、heading、global/root trajectory 任一轴明显退化；或 decoded physical/visual evidence 出现明显失败。
- **continue**：相对 Parent 不出现 semantic/distribution broad regression，且 RA pose、heading、global/root 形成 Pareto 改善或严格非劣，并通过固定样本与 blind physical-quality review。
- Stage2 screen 通过只授权讨论 Human continuation，不自动授权 joint、Unified 或 VACE 训练。

> [!failure] P0-H128-S2 screen decision：stop
> 30K 与 35,006 使用同一 first-512 ordered IDs（SHA256 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`）、seed17、DDIM50、CFG 1、C3-25 owning decoder 与 official Human evaluator。35,006 相对 30K 有恢复，但 FDTMR、TMR、HCov、RA pose、heading、global 与 root 仍全部触发 broad-regression stop 条件；no-reference kinematic diagnostic 同时显示 generated acceleration、jerk 与 foot-skate heuristic 远离同 ID dataset reference。两个 raw result SHA256 分别为 `0a8a346f40b89bc03ecfe514b213ccc40567bbaf06594dd78a9fcd526655a7f6` 与 `b6c303c24ae3d94e44cf3bd85a988bd503b51fafa0bb65358d0b1a3670d34ecc`；固定样本数组已导出，匿名视觉包与人工 verdict 不改变已由 canonical decoded fields 触发的 stop。

该结果只增强“Stage2 architecture、inductive bias、objective 与 C3 latent topology 之间存在不匹配”的假设。它不能把根因收缩成参数容量不足：P0-H128-S2 参数量与 Parent 近似，且本 screen 同时改变了一个不可拆的 Human-only topology package。

## 5. Human hard gate 与 Unified 恢复条件

最终 single-Human generator 必须同时满足：

- FDTMR、TMR 与 HCov 相对 Parent 不出现 broad regression；
- root-aligned pose、heading、global/root trajectory 形成 Pareto 改善或严格非劣；
- 固定样本视觉质检通过；
- blind/no-reference Human physical-quality 质检通过；
- no-reference decoded physical fields 与视觉质检没有明显失败。

Stage1 reconstruction screen 本身不能满足本 gate。未同时满足时保持新的 joint、Unified 与 VACE 训练暂停。只有 single-Human hard gate 通过、同一 frozen Human source 可被 Camera 分支消费且 joint parallel 不回退时，才允许在新的独立 contract 中讨论恢复 Unified。

## 6. Closure index

- P0-JC architecture/view arms 与 Tb25：已关闭；结果归 [[StoryMotion-valid-metric-ledger]]，完成/失效事件归 [[version_family]]，历史协议见 [[archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder_closed-through-human-only_20260724]]。
- Human-only native `0→105K` 与 learning-curve screen：已关闭且不晋升；结果归 [[StoryMotion-valid-metric-ledger]]，run artifact 位于 `runs/train/stage2/p0_c3_25_human_only_native_0_105k_seed17_5090g2_20260723/` 与其对应 eval run。
- P0-HATTR-1 / P0-HARCH-0 / targeted Stage1 Camera probe / P0-HCAM-S2 与 Human128 Stage1/Stage2 preflights：均为 no-update 且已闭合；数值只见 [[StoryMotion-valid-metric-ledger]]，hash 与 immutable roots 只见 [[Storymotion-exp-sha]] 及对应 run root。
- P0-HVIEW-1：`superseded_before_launch`；没有 checkpoint、optimizer 或 metric。其被替代事件只见 [[version_family]]。
- P0-H128-S2 first attempt：在 checkpoint 前安全停止且不复用；fresh `r2` 独立运行。失败与启动事件只见 [[version_family]]。
- P0-H128-S2 fresh `r2`：30K 与 35,006 N=512 screen 均触发 stop；不继续 105K，不授权 joint-only extension。后续外部 system control 与 matched-backbone preregistration 已归档至 [[archived/experiments/2026-07-25_storymotion-v9-external-system-backbone-adaptation-closed]]。
- E1 G-SYS-H：Stage1 `30K` pure4,053 reconstruction floor 通过；Stage2 `105K` N=512 Human generation 因 semantic/coverage broad regression 停止。两种 verdict 不跨 Stage 合并，且 E1 仍是 full-system control。
- E2 D-SYS-C：正确 train-only MinMax 的 `105K` N=512 observed-Human Camera completion 相对旧 5K 明显恢复，但相对 C3 Direct-C 在语义、coverage、trajectory 与 rotation 上 broad regress，停止；不是 joint evidence。
- E3 C3-D-DC：fixed-C3 `105K` N=512 Direct-C 的 trajectory/rotation 改善而 semantic/coverage 回退，按 matched gate 停止；该 trade-off 不授权 joint extension，也不证明 backbone capacity ceiling。
- E5 C3-MARDM-H：fixed-C3 Human-only N=512 已闭合；支持 system-level generation-capability pass，但 strict physical gate 未闭合，且 topology、objective、sampler 同时变化。
- E6 ViMoGen-light：CLIP 与 UMT5 fixed-C3 Human-only N=512 已闭合；CLIP 是综合较强 endpoint，UMT5 只在 HCov 更高；两者都不产生 Camera/joint 或 pure-backbone claim。
- P0-H128-S1：first attempt 因 contract logical-path 违规安全停止且不复用；fresh `r2` pure4,053 short 无 Pareto，paired uncertainty 只确认 heading 稳定退化，按 gate 停止且不做 full/cache/Stage2。它是独立 Stage1 system screen，不与 P0-H128-S2 混成一个 causal arm。
- C3-25 mainline selection：已闭合；formal evidence 归 [[StoryMotion-valid-metric-ledger]]，最终事件归 [[version_family]]。

## 7. Evidence routing

- 运行前：本页只拥有 causal question、变量与 gate；精确 mutable provenance 写入 `experiment_contract.json`。
- 运行中：进度、ETA、stderr/stdout 与临时状态只写 run manifest/log。
- screen 结束：raw artifact 保留在 `runs/`，本页只更新对应 decision 状态。
- formal audit：数字只登记一次到 [[StoryMotion-valid-metric-ledger]]，hash 与 immutable identity 只登记到 [[Storymotion-exp-sha]]；[[current]] 只更新简短当前裁决，[[version_family]] 只记录 finalized event。
