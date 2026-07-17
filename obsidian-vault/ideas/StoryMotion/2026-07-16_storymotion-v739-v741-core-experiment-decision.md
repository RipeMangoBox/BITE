---
title: "StoryMotion Core Experiment Execution"
status: active
hypothesis: |
  v7.14 的长序列human误差已定位到累计heading。当前在4090并行执行三条matched non-causal Stage1 system controls：v8.1A human199 geometry loss、v8.1B residual AE与v8.2 human200；三条endpoint后由GPU1串行执行pure4053 geometry。v8.3因22:00 gate未满足而保持零进度；研究结论与公平比较由version.md持有。
tags:
  - StoryMotion
  - experiment
  - execution
  - status/active
aliases:
  - StoryMotion-Core-Experiment-Execution
source_notes:
  - "[[version]]"
  - "[[history]]"
  - "[[2026-07-12_storymotion-valid-metric-ledger]]"
  - "[[2026-07-17_storymotion-stage1-length-condmdi-causal-priority]]"
  - "[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]"
  - "[[2026-07-17_storymotion-v8-3-data-curation-progress]]"
created: 2026-07-16T01:30:00+0800
updated: 2026-07-17T18:25:00+0800
---

# StoryMotion Core Experiment Execution

> [!abstract] 2026-07-17 18:25 CST
> git、远端同步、stats 与 contract preflight 已闭合。4090 GPU0 共驻 v8.1A/B，GPU1 运行 v8.2 human200；最近5k吞吐分别为 `15.55/12.14/18.81 step/s`，三条 train/test/grad/checkpoint 均 finite。按实测吞吐，v8.2/A/B 连同 queued pure4053 geometry 预计分别在 07-18 03:40–04:20、04:45–05:20、08:15–09:15 CST 闭合。v8.3 的“v8.2在当日22:00前完整完成”条件不成立，清洗未启动且所有进度计数为0。

本页不再复制 v7.39–v7.43 的研究叙事、P0-G 假设或完整 metric table。当前结论见 [[version]]，精确数值见 [[2026-07-12_storymotion-valid-metric-ledger]]，版本 provenance 见 [[history]]。

## 1. 活动运行快照

| priority / run | host / GPU | 最近一次可核验证据 | 收敛与健康判断 | 自动下一步 | 预计全部完成 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| P0 / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | 4090 / GPU0 | step `54,441/636,000`；近5k=`15.55 step/s`；train total=`0.01751`；test step54k=`0.02645` | frozen yaw/root=`0.001/0.003`；train/test/grad finite；matched `81.38M` contract | endpoint→GPU1 pure4053 geometry；不自动建cache | 07-18 04:45–05:20 CST | 进行中 |
| P1 / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | 4090 / GPU0 | step `29,268/636,000`；近5k=`12.14 step/s`；train total=`0.03486`；test step28k=`0.07109` | AAMMARDM-style non-causal residual AE；从零训练；train/test/grad finite | endpoint→GPU1 pure4053 geometry；按system comparison解释 | 07-18 08:15–09:15 CST | 进行中 |
| P1 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | 4090 / GPU1 | step `6,133/636,000`；近5k=`18.81 step/s`；train total=`0.05389`；test step4k=`0.11265` | stats SHA=`70623ea…5011`；checkpoint内嵌human200/camera-first/non-causal contract；preflight passed | endpoint→同GPU pure4053 geometry；通过gate后才允许cache | 07-18 03:40–04:20 CST | 进行中 |
| AUTO-EVAL / `v8_stage1_posttrain_eval_g1_20260717` | 4090 / GPU1 queue | tmux存活；顺序=`v8.2 → v8.1A → v8.1B`；等待`status=trained`与endpoint checkpoint | 只等待，不占GPU；单条失败不阻止后续条目 | 对三条各执行ordered pure4053、四长度桶、human/root/yaw/camera geometry | 随各endpoint后约2–4分钟 | 等待 |
| P1 / v8.3 curation | 不占GPU | plan/progress已创建；gate=`v8_2_full_endpoint before 22:00` closed | processed/annotated/quarantined/manifests/jobs=`0` | v8.2 endpoint核验后另开执行窗口 | 未启动 | waiting_on_v8_2_endpoint |
| P0 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | 5090 / 仅GPU0 | 18:28 CST step=`46,700/105,000`；loss=`0.12826`；grad=`0.18530` | 原driver继续，finite；本轮未修改 | endpoint后由其既有driver闭合formal | 既有driver管理 | 进行中 |

ETA 按当前实测吞吐与既有 formal 时长估算，不是调度承诺。PID 只属于瞬时快照；manifest、checkpoint、contract 与 eval artifact 才是完成证据。

## 2. Director-C 完成分析

### 2.1 训练闭环

- `94/94` epochs，endpoint global step `239136/239136`，train samples `162,760`，shuffle 开启。
- 实际 sample exposures `15,299,440`，相对预注册 `15.36M` 少 `0.394%`；属于 exposure-matched fixed-budget endpoint。
- checkpoint selection 明确为 `fixed-budget endpoint only`；fit 中没有构造 formal test dataset，dev 为 train-only derived 256。
- endpoint checkpoint SHA256：`ad27564052465ff11f5264c5606473f2daacaaf74abbf45adc7b563328b5e823`。
- contract SHA256：`3a3635be17fa1c6cc155fa8e5ad7339d46e446c55195ec9ca1b350390addcaa1`。
- 训练末段 loss 与 dev loss 都保持 finite；已观测 dev last 约 `0.02407`、best 约 `0.02255`，没有持续发散或明显 endpoint overfit 证据。

### 2.2 Formal 闭环

- scope=`formal_pure4053`，sample count `4,053`，seed `17`，batch `64`。
- sample-ID SHA256：`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，与 StoryMotion formal pure set 一致。
- 4,053 records、4,053 unique IDs、sample indices `0..4052`；64 个 bridge batches 全 finite。
- rotation determinant 位于 `[0.999, 1.001]`，orthogonal error 小于 `1e-3`；GT Pulp intrinsics 与 official camera callback 绑定正确。
- formal metrics：FDCLaTr `32.4365`、CLaTr `52.6617`、CCov `81.49%`、Caption F1 `0.6884`。
- formal JSON SHA256：`f9693592d62780dd2a4ed330dc2b102b88b775a839e459c6adefc6eb2bd97b15`；eval elapsed `690.65s`。

第一次用 training runtime 执行 eval contract 时被 runtime-role gate 正确拒绝；切换到冻结的 eval runtime 后完整通过。这是环境隔离生效，不是实验失败。

### 2.3 公平性裁决

Director-C 与 StoryMotion L0 共享 pure sample IDs、official Pulp camera callback、seed 与近似 exposure budget，因此是可入论文的 native-system camera peer。它们仍有以下主动差异：

- Director-C 的 human condition 是 GT Pulp SMPL pelvis translation trajectory；L0 使用 complete GT-H latent。
- Director-C 直接预测 9D rot6d+translation trajectory 并解码为 C2W，不经过 v7.14 tokenizer。
- Director-C 使用 native EDM10、guidance `1.4`；L0 使用 DDIM50、CFG `1`。

因此 Director-C 只支持 system-level Pareto：相对 L0，它改善 FDCLaTr 与 CCov，但降低 CLaTr 与 Caption F1。完整三模式表与结论统一见 [[version#3.2 Camera completion]]。

## 3. Hard gates 与自动衔接

### 3.1 MotionLab-MFT

只有同时满足以下条件才启动 formal：

1. train launcher 正常退出；
2. `manifest.json.status == trained`；
3. `train/last.pt` 存在且非空；
4. contract、sample IDs、non-causal v7.14 Stage1 与 official human callback audit 通过。

任一条件失败都 hard fail；不得将半程 checkpoint、smoke 或 screen 填入 human comparison placeholder。

### 3.2 v7.43 B/C

- B 从原 symmetric B30 严格恢复 optimizer，保持 `joint_loss=1`、`coupling=1/symmetric`，只报告 H/C/parallel。它的 symmetric human 路径观察 camera latent，不进入 human-text-only主表。
- C 从原 no-joint C30 严格恢复 optimizer，保持 `joint_loss=0`、fixed denominator、human-first，只报告 H/C/cascade，不报告未训练的 parallel。
- 两条 driver 都必须在 step105k、posthoc tracking、strict exposure/optimizer check 与 contract audit 全通过后才逐 profile formal。

截至 20:04，B/C 均已满足全部 gate并完成。B 的 routing 裁决见 [[2026-07-12_storymotion-valid-metric-ledger#17.5 v7.43-B final-budget symmetric attribution]]；C 的 no-joint 裁决见 [[2026-07-12_storymotion-valid-metric-ledger#17.6 v7.43-C final-budget no-joint attribution]]。C 的三条 formal 绑定同一 checkpoint `c70a44c…0626`、同一 pure ID hash 与 owning decoder，H/C/cascade 均广泛弱于 L0，包含 cascade Out `+3.99 pp`。

### 3.3 MoMask-Pulp

- upstream base=`94a6636c9c46…`，当前适配 HEAD=`09f3068d820e…`；clean branch=`storymotion/pulp-human-baseline`。
- train=`162,760`，ordered ID SHA256=`a0981b6c…51dc9`；pure placeholder=`4,053`，ID SHA256=`a0d7627e…6b93`；fit 仅构造 train cache。
- representation=Pulp normalized human199；condition=human text only；RVQ 与 Mask/Residual Transformer 均 non-causal。
- VQ 固定 `159k × 512 = 81.408M` exposures，与 v7.14 Stage1 的 `636k × 128` 对齐；Mask、Residual 各固定 `240k × 64 = 15.36M` generation-component exposures。不使用 validation/test 选 checkpoint。
- 首次直接读取 HDD 小 `.npy` 的队列因 I/O starvation 主动终止，未产出 checkpoint，也不算模型失败。packed revision 将同一 ordered train split 写入 SSD 并分别校验 data/offset/length/caption SHA256；production-batch smoke 与正式 VQ 已通过。
- 30k 的原依据只是 `30000 × 512 = 15.36M`，误把 generation-component budget 用到了 tokenizer；它既不对齐 Pulp Stage1，也触发不了 MoMask 的 150k LR milestone。该 run 已在 last logged step `13200` 停止，完整 checkpoint step=`10000`，Mask/Residual 从未启动；`ABORTED_BUDGET_CORRECTION.json` 禁止晋级。
- revised adapter HEAD=`09f3068d820e…`；contract SHA256=`a55c61a6994800c1c932bbfb2970a9f1f79089d019e157c1bad8af7f9e2b0868`；cache metadata 继续复用同一 verified train-only artifact。
- formal 必须等待三阶段 fixed endpoint 与 integrity marker 全部完成；smoke、VQ 半程或单组件 endpoint 均不得填 human comparison row。

### 3.4 结果到达后的唯一动作

1. 把 exact metrics、checkpoint 与 artifact 先写入 canonical ledger；
2. 填充 [[version#3. StoryMotion 与 baseline/specialist 的公平对比]] 的对应 placeholder 或 claim 状态；
3. 更新 [[history]] 的可靠性结论；
4. C 与 CCD-Pulp 已出表；MotionLab/MoMask formal 到达后进入 Stage1 representation / Stage2 backbone 根因矩阵，不直接锁 seed17 recipe；
5. 新 treatment 只需通过 direct H、direct C 与 joint parallel hard gate；cascade 不再阻塞。通过后才在空闲的 5090 GPU0 从零启动 seed23。P0-G、temporal variant、residual/adapter 与更多 baseline 不自动启动。

### 3.5 CCD-Pulp

- 方法来自 Director 论文正式对比的独立 CCD baseline，而不是 Director-A/B 消融；upstream=`79b4564b…`，adapter=`3b012a9…`。
- fixed representation 为 corrected v7.14 non-causal latent 与 owning decoder；任务输入是 complete GT-H latent + camera text，输出只含 camera latent。
- 固定训练预算 `60k × 256 = 15.36M`，fixed endpoint only；formal 预注册 DDIM50、CFG `2`、`eta=0`、seed17、pure `4,053` 与 official camera callback。
- production-batch smoke、Git bundle/SHA256、train/eval cache、train-only full-cov stats、owning checkpoint/decoder 双 SHA 与 N64 official-callback bridge 均通过。corrected run 已从 step0 完成 fixed endpoint 与 formal；首次缺 decoder SHA 的旧 run 保持不可晋级。
- formal：FDCLaTr `101.03`、CLaTr `33.095`、CCov `59.91%`、Caption F1 `0.442`；相对 L0 四项均回退。精确 artifact hashes 与差值见 [[2026-07-12_storymotion-valid-metric-ledger#17.7 CCD-Pulp fixed-endpoint audit]]。

## 4. 已完成队列与当前决策

| item | artifact 状态 | promotion / claim 状态 |
| --- | --- | --- |
| v7.40 full-sequence RF 30k + four-profile pure4053 | 已完成、strict audit 通过 | formal promotion 未通过；只保留 semantic/recall Pareto |
| v7.42 H/C/J same-implementation specialists | 三条 pure4053 已完成 | shared-training joint benefit；三模式全面非劣未成立 |
| corrected Director-C | endpoint + screen + pure4053 formal 已完成 | 合法 native camera peer；与 L0 Pareto |
| v7.43 B | endpoint + H/C/parallel pure4053 formal 已完成 | 支持 asymmetric routing；symmetric human 不入 human-text-only 主表 |
| v7.43 C | endpoint、posthoc、contract、H/C/cascade pure4053 formal 已完成 | 三种输出全面回退，支持 joint exposure；5090 GPU0 已释放 |
| v7.14 full-sequence length audit | pure4053、paired official AE、length bins与script/checkpoint provenance完整 | 排除 64-frame crop叙事；确认 local human length-generalization/root-drift风险 |
| CondMDI official all-mask smoke | HumanML3D 750k checkpoint、zero mask与saved result hash已核验 | 证明 released conditional checkpoint具备纯 text-to-motion sampling路径；不产生跨数据质量结论 |
| MotionLab-MFT | 已部署且正常训练 | 等 representation-matched human peer |
| MoMask-Pulp | train cache、revised Git/data/budget contract、smoke 已通过；Stage1-matched 三阶段长训已部署 | 等 native-operator human peer fixed endpoints 与 formal；30k screen 禁止晋级 |
| CCD-Pulp | clean Git/archive、contract、fixed endpoint 与 pure4053 formal 已完成 | L0 四项 camera 主指标均占优；不追加 tuning/seed |

P0-G 的唯一状态在 [[version#4. P0-G：raw/decoded auxiliary 的唯一状态]]；本页不再另设 `P0-R` 或复制 raw-loss 假设。

## 5. Director 旧证据清理 provenance

2026-07-16 已删除 18 个旧 Director 无效对象，共 `52,838,886,783` bytes：数值发散或 test-as-validation 的训练/评测目录、caption/character shuffle 派生视图、废弃 adapter scaffold，以及两份实际读取 StoryMotion checkpoint 却命名为 E.T./Director 的 JSON、records、logs/marker。删除前相关旧 run 均无打开 FD，删除后逐项验证不存在。

保留对象只有 corrected Director-C run、pure view、DIRECTOR repo、冻结 runtime audit 与必要的 launch provenance。旧错误数值不得恢复、不得作为 placeholder、不得与本次 formal 合并。

## 6. Evidence roots

- 4090 v8.1A：`runs/stage1/v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717/`
- 4090 v8.1B：`runs/stage1/v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717/`
- 4090 v8.2：`runs/stage1/v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717/`
- 4090 v8.2 train-only stats：`runs/train/stage1/stats/v8_2_human200_ae_train_split_20260708.json`
- 4090 v8 post-train queue log：`logs/v8_stage1_posttrain_eval_g1_20260717.log`
- 4090 MotionLab：`runs/stage2/baseline_motionlab_mft_v714_human_seed17_4090g0_20260716/`
- 4090 MotionLab watcher：`runs/stage2/baseline_motionlab_mft_v714_human_seed17_4090g0_20260716/posttrain_formal_eval.queue.log`
- 4090 v7.43 B：`runs/stage2/v7_43_p0b_sym_lr3em5_105k_purefull_seed17_4090g1_20260716/`
- 5090 v7.43 C：`runs/stage2/v7_43_p0c_asym_nojoint_lr3em5_105k_purefull_seed17_5090g0_20260716/`
- v7.43 drivers：`runs/queues/v7_43_final_budget_controls_20260716/`
- 5090 Director-C：`/data/public/ripemangobox/Motion/baselines/runs/director_c_pure_matched_seed17_5090g3_20260716/`
- 5090 MoMask-Pulp current：`/data/public/ripemangobox/Motion/baselines/runs/momask_pulp_human_native_seed17_5090g3_stage1matched_20260716/`
- 5090 MoMask-Pulp invalidated 30k screen：`/data/public/ripemangobox/Motion/baselines/runs/momask_pulp_human_native_seed17_5090g3_packed_20260716/`
- 5090 MoMask repo：`/data/public/ripemangobox/Motion/baselines/MoMask_storymotion_20260716/`
- 5090 MoMask packed train cache：`/home/ripemangobox/.cache/storymotion_baselines/momask_pulp/train_a0981b6c_b88f16ca/`
- 4090 CCD-Pulp run：`/data/public/ripemangobox/Motion/baselines/runs/ccd_pulp_camera_completion_v714_seed17_4090g1_20260716/`
- 4090 CCD repo：`/data/public/ripemangobox/Motion/baselines/Camera-control_storymotion_20260716/`
- 4090 CCD Git archive：`/data/public/ripemangobox/Motion/StoryMotion/logs/git_archives/20260716T120028Z_ccd_pulp_camera_peer_4090_3b012a934469/`
- 4090 CCD invalidated pre-contract run：`/data/public/ripemangobox/Motion/baselines/runs/ccd_pulp_camera_completion_v714_seed17_4090g1_20260716_invalid_missing_decoder_hash/`
- 5090 v7.14 full-sequence audit：`runs/train/stage1/v7_14_official_contract_20260710/joint_ae_official_4090_gpu0_r2/eval/long_sequence_geometry_pure4053_paired_20260717.json`
- 4090 CondMDI all-mask result：`/data/public/ripemangobox/Motion/CondMDI/save/results/storymotion_condmdi_randomframes_allmask_text_20260717/results.npy`
- 4090 Top-5 Pulp summary：`runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_joint_top5_20260716/comparison_geometry_pulp/render_summary.json`
- Director train result：`.../train_result.json`
- Director formal：`.../eval/formal_pure4053.json`
- Director contract：`.../experiment_contract.json`
- v7.42 specialists：`runs/stage2/v7_42_l0_sameimpl_specialist_seed17_{human,camera,joint}_exposure_matched/`
- v7.40 formal：`runs/stage2/v7_40_molingo_fullseq_rf_matched_seed17_5090g0_20260715/eval/official_pure4053_rf50_cfg4_step30000/`

## 7. Baseline Git provenance

所有 baseline 源码均已生成非破坏性恢复包：`repository.bundle`、committed tree、working-tree patch、untracked source archive/inventory、restore instructions 与 `SHA256SUMS`。既有 archive root 为 `/data/public/ripemangobox/Motion/baseline_provenance/git_archives/`；CCD-Pulp 本次恢复包位于 StoryMotion 的 `logs/git_archives/`，精确路径见 evidence roots 与下表。

| repository | host | archived HEAD | archive package | 状态 |
| --- | --- | --- | --- | --- |
| StoryMotion | 5090 / 4090 | `37475ebc19ef…` | `20260716T100532Z_storymotion_{5090,4090}_37475ebc19ef` | SHA256 verified |
| Director | 5090 | `63fa65276142…` | `20260716T100532Z_director_5090_63fa65276142` | SHA256 verified |
| MotionLab | 4090 | `8b2f7b35ae57…` | `20260716T100532Z_motionlab_4090_8b2f7b35ae57` | SHA256 verified |
| MoLingo | 5090 / 4090 | `52e3b4c30925…` / `86e21b24784e…` | 对应 `20260716T100532Z_molingo_*` | SHA256 verified |
| PulpMotion | 4090 | `b81c7d95f451…` | `20260716T100532Z_pulpmotion_4090_b81c7d95f451` | SHA256 verified；5090 copy 为 non-git mirror |
| MoMask-Pulp current | 5090 | `09f3068d820e…` | `20260716T110713Z_momask_pulp_stage1matched_5090_09f3068d820e` | clean commit；bundle/head/SHA256 verified |
| MoMask-Pulp 30k screen | 5090 | `4fffe83f4f74…` | `20260716T103840Z_momask_pulp_packed_5090_4fffe83f4f74` | archived；budget-invalidated，不可晋级 |
| CCD-Pulp | 4090 | `3b012a934469…` | `20260716T120028Z_ccd_pulp_camera_peer_4090_3b012a934469` | clean commit；bundle/head/SHA256 verified；owning decoder hash in run contract |

MoMask 的 upstream base commit=`94a6636c9c463b7a9414c3401a6f1b67e6c51824`，OpenAI CLIP source commit=`d05afc436d78f1c48dc0dbf8e5980a9d471f35f6`；运行 contract 另保存完整 `pip freeze`、PyTorch/CUDA/cuDNN 与 GPU 型号。未来新增 baseline 必须先 commit 或完整 archive，随后才允许 preflight/long train。
