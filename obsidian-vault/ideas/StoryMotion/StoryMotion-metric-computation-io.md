---
title: "StoryMotion Metric Computation IO"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - metric
  - evaluation
  - status/active
aliases:
  - StoryMotion-Metric-IO
source_notes:
  - "[[StoryMotion/current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[archived/evidence/2026-07-11_storymotion-v7.14-corrected-results]]"
  - "[[archived/evidence/2026-07-12_storymotion-v7.17-decoder-cache-contract-execution]]"
created: 2026-07-09T12:20:00+0800
updated: 2026-08-03T15:13:03+08:00
---

# StoryMotion Metric Computation IO

> [!abstract] Scope
> 本页说明 StoryMotion canonical decoded metric 与当前 Stage1／Stage2 training objective 如何计算、吃什么输入、输出什么键。Stage1 true-length paired reconstruction、Stage2 decoded generation 与 optimizer objective 是三个不同 protocol，必须分开解释。核心 official generation 指标来自 PulpMotion callback；StoryMotion 本地脚本负责 owning decode、I/O bridge 与补充 paired/physical schema。归一化 feature-space loss 与 optimizer 过程数值只用于训练诊断，不属于正式 ranking。

## 1. Evaluation Data Contract

Stage1 canonical true-length reconstruction eval 入口：

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_joint_tokenizer_official_recon.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/evaluate_c3_formal.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/evaluate_formal_v3.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/evaluate_humanml_formal_v2.py
```

Stage2 official eval 入口：

```text
linkedCodebases/StoryMotion/scripts/storymotion_official_full_eval.py
```

PulpMotion official metric 源码路径在 4090 worktree：

```text
/data/public/ripemangobox/Motion/StoryMotion/linked/PulpMotion/src/callbacks/human_metrics.py
/data/public/ripemangobox/Motion/StoryMotion/linked/PulpMotion/src/callbacks/camera_metrics.py
/data/public/ripemangobox/Motion/StoryMotion/linked/PulpMotion/src/callbacks/joint_metrics.py
/data/public/ripemangobox/Motion/StoryMotion/linked/PulpMotion/src/metrics/*.py
```

Official callback 输入 contract：

| object | shape / type | producer | consumer | meaning |
| --- | --- | --- | --- | --- |
| `batch["padding_mask"]` | bool, `B x T` | PulpMotion dataset | all callbacks | valid-frame mask; padded frames excluded |
| `batch["tmr_caption"]`, `batch["tmr_mask"]` | text feature sequence | PulpMotion dataset | human metrics | human caption DistilBERT / TMR text input |
| `batch["clatr_caption"]`, `batch["clatr_mask"]` | text feature sequence | PulpMotion dataset | camera metrics | camera caption CLIP / CLaTr text input |
| `batch["camera_segments"]` | per-frame class labels | PulpMotion dataset | camera segment metrics | camera event / movement labels |
| `batch["proj_joints"]` | `B x T x 18` | PulpMotion dataset | joint metrics | GT 2D projection of 9 selected joints, flattened xy |
| `outputs["raw_input"]` | official raw GT | eval script / PulpMotion dataset | all callbacks | reference human, camera, intrinsics |
| `outputs["raw_output"]` | official raw prediction | StoryMotion decode bridge | all callbacks | generated or reconstructed human/camera/intrinsics |
| `outputs["x_output"]` | feature-space output dict | model / bridge | joint metrics optionally | may contain direct projection; often absent in Stage1 |

Stage1 reconstruction-specific policy:

- Each sample is reconstructed at its true valid length, then padded back into the official batch shape.
- Non-causal tokenizers therefore do not see future padding zeros during reconstruction.
- Training is not fixed-first-64: C3-25 and redesigned Pulp collators use `fixed_max_frames=0`; HumanML preprocessing uses max-300/stride-240 windows plus a tail-aligned final window.
- Reconstructed human features are decoded to official human raw joints by `feature_dataset.human_dataset.get_raw`.
- Reconstructed camera features are converted from StoryMotion camera features to camera poses by `camera_features_to_poses`.
- Official callbacks then run unchanged.
- HumanML3D partial controls must label joint rot6D channels `4:136` as missing/imputed when only root/local fields are observed. Their evaluator may report paired root/local geometry, but must not emit rot6D, Camera, projective, semantic-generation, or joint claims. Historical artifact key `pose6d_policy` is a legacy name for this rot6D boundary.

### 1.1 StoryMotion Feature Representations

The names below describe the tensors that enter a Stage1 tokenizer. They are
not interchangeable merely because a tensor has a similar width. A Stage2
cache always inherits its parent Stage1 feature contract, normalization, and
owning decoder.

| representation | width | raw semantic layout | temporal/integration consequence | decoder boundary |
| --- | ---: | --- | --- | --- |
| raw human199 | 199 | root height `z[0]`; local-root XY velocity `[1:3]`; yaw increment `Δψ[3]`; pose rotation 6D `[4:136]`; local joints `[136:199]` | Global yaw is `cumsum(Δψ)`; world root XY rotates the local velocity by that yaw and then integrates it. A small per-frame yaw error can therefore become a long-sequence global error. | Pulp RIFKE human decoder owns the raw-joint reconstruction. |
| normalized human199 | 199 | The same human199 after Pulp train-split per-channel affine normalization. | The normalized channels are what v7.14/v8.1 Stage1 reconstructs; integration must happen after de-normalization. | The corrected local decoder or the frozen official Pulp decoder must match the checkpoint/cache contract. |
| human200 | 200 | root height `z[0]`; root XY relative to the first frame `[1:3]`; global yaw as `sin ψ, cos ψ` `[3:5]`; pose rotation 6D `[5:137]`; local joints `[137:200]`. | Root XY and yaw are direct rather than recurrent. Its owning inverse unwraps yaw and differences root XY back to human199 before the Pulp callback. | v8.2 owns separate train-only 200D statistics and this inverse; it cannot consume a human199 cache or decoder by name alone. |
| camera9 | 9 | c2w camera translation `[0:3]` plus rotation 6D `[3:9]`. | Absolute pose per frame; it has no FOV, human-relative distance, or explicit translation-velocity channel. | Legacy local camera decoder only; it is a control, not the v7.14 mainline camera contract. |
| official camera14 | 14 | FOV `[0:2]`; normalized camera-center minus human-root distance `[2:5]`; c2w rotation 6D `[5:11]`; normalized frame-to-frame c2w translation velocity `[11:14]`. | The official decoder cumulatively sums the de-normalized velocity to form the camera trajectory, then adds the first-frame reconstructed human-root plus relative-distance origin. Thus the last three channels are an integration-sensitive path even though the representation also contains direct relative-distance information. | Pulp `traj+char+proj` joint decoder owns raw pose/intrinsics conversion and is required for official camera metrics. |

Important distinctions:

- `camera14` velocity is a c2w translation difference, not the human's local
  root velocity. A camera path loss must reproduce the official decoder's
  first-frame origin and cumulative-velocity semantics; comparing only the
  14D feature MSE would miss trajectory drift.
- `camera14[2:5]` is expressed relative to the decoded human root. Its
  first-frame value participates in the raw camera origin, so human and camera
  reconstruction errors can couple at decode time even when the camera branch
  loss is unchanged.
- The zero-valued first camera velocity frame is a convention, not a learned
  absolute origin. The Stage1 loss masks that frame for the velocity channels.
- The Paper A C1REL control uses the complete pose
  $\widetilde T_{C,t}=T_{C,1}^{-1}T_{C,t}$: the three-dimensional translation
  vector and relative rotation are retained, together with relative velocity
  and FOV. A scalar distance is not a valid substitute because it removes
  left/right and in/out signs. Human128 plus interaction16 own the missing
  initial Human-relative anchor through that checkpoint's Camera14 decoder.

### 1.2 Representation by StoryMotion Version Family

This table records representation families, not a ranking. Every comparison of
results must still name the exact `version / run`, checkpoint, cache, and
decoder in the metric ledger.

| version / family | human representation | camera representation | owning decoder / comparison status |
| --- | --- | --- | --- |
| pre-v7.14 local tokenizer controls, including v7.6–v7.8 and v7.32 | raw human199 | camera9 absolute c2w | Legacy local decoder; not comparable to corrected v7.14 official rows. |
| v7.20 raw14 control | raw human199 | raw official-camera14 semantics | Local control for normalization/contract diagnosis; not the mainline representation. |
| v7.33 separate-tokenizer control | normalized human199 | official camera14 | Separate owning decoders; Stage1-only control, not a Unified cache promotion. |
| v7.14 corrected Stage1; v7.17 cache; v7.34–v7.38 Unified L0 lineage | normalized human199 | official camera14 | Corrected non-causal local joint AE plus its owning local decoder. This is the current StoryMotion mainline representation. |
| v7.46–v7.47 frozen official-AE control | normalized Pulp human199 | official camera14 | Frozen official Pulp AE and official owning decoder; representation-matched control, never relabel as the v7.14 local AE. |
| v8.0 attribution | normalized human199 | official camera14 | No new representation training; channel-oracle and deep-AE diagnostics only. |
| v8.1A | normalized human199 | official camera14 | Same v7.14 architecture/representation, with decoded cumulative-yaw and world-root auxiliary losses; non-promotion candidate. |
| v8.1B | normalized human199 | official camera14 | Same feature contract but residual-AE architecture; non-promotion control. |
| v8.2 | human200 with its own train-only normalization | official camera14 unchanged | Own human200 inverse plus Pulp camera14 decoder; candidate/control, not a v7.14 cache replacement. |
| v9 H-ANCHOR-S1 Pulp-only matched control | normalized Pulp human199；the Camera-free `pulp_anchor` role supervises root/yaw/local only，while the `pulp_joint` role supervises full Human199 | official camera14 only in `pulp_joint` batches；the two roles use the same ordered Pulp identities | Exact non-causal checkpoint decoder with per-sample true-length reconstruction；Stage1 representation diagnostic only，not a mainline promotion. |
| v11 C0-LAT／C0-GEO shared Stage1 | normalized Pulp human199；Human128 owner | official Camera14 through interaction16＋camera48 | Exact v9 Pulp-only non-causal checkpoint and owning `D_h/D_c/D_f`；current co-mainline Stage1 owner. |
| Paper A HREL-w/o-Interaction16 | normalized Pulp human199；Human128 | v9 HREL Camera14 through Camera48；no interaction16 | Fresh matched 176D Stage1 and its owning decoder；active representation ablation, no formal result yet. |
| Paper A C1REL | normalized Pulp human199；Human128＋interaction16 relation owner | full first-Camera-frame-relative translation vector／rotation／velocity／FOV through Camera48 | Fresh parameter-matched 192D Stage1；owning joint decoder restores Camera14 initial anchor；active representation control, no formal result yet. |

Stage2 rule: a cache built from any row above is valid only with that row's
exact Stage1 checkpoint, representation normalization, latent order, and
owning decoder. Equal nominal latent width does not authorize weight or cache
reuse.

## 2. Human / TMR Metrics

PulpMotion implementation:

```text
linked/PulpMotion/src/callbacks/human_metrics.py
linked/PulpMotion/src/metrics/encoders/tmr.py
linked/PulpMotion/src/metrics/frechet.py
linked/PulpMotion/src/metrics/prdc.py
linked/PulpMotion/src/metrics/similarity.py
linked/PulpMotion/src/metrics/retrieval.py
```

Human raw preprocessing:

1. Take `outputs["raw_input"].joints` and `outputs["raw_output"].joints`.
2. Keep the first 22 joints.
3. Apply coordinate transform `[[1,0,0],[0,0,1],[0,1,0]]`, then flip x.
4. Convert valid frames to Guo motion features by `joints_to_guofeats`.
5. Normalize with TMR `mean.pt` / `std.pt`.
6. Encode reference motion, generated motion, and text into 256-d TMR latent vectors.

| display name | output key | input pair | computation | direction |
| --- | --- | --- | --- | --- |
| FDTMR | `test/tmr/ftd` | generated TMR motion embeddings vs reference TMR motion embeddings | Frechet distance between two Gaussian fits in TMR latent space | lower better |
| TMR | `test/tmr/tmr_score` | generated TMR motion embedding vs TMR text embedding | cosine similarity, summed over samples, scaled by `100`, clamped at zero | higher better |
| HCov | `test/tmr/coverage` | generated vs reference TMR motion embeddings | PRDC coverage: fraction of real samples whose nearest fake is inside the real sample's kNN radius; `k=3`, averaged over 5 chunks | higher better |
| TMR precision | `test/tmr/precision` | generated vs reference TMR motion embeddings | PRDC precision in TMR space | higher better |
| TMR recall | `test/tmr/recall` | generated vs reference TMR motion embeddings | PRDC recall in TMR space | higher better |
| TMR density | `test/tmr/density` | generated vs reference TMR motion embeddings | PRDC density in TMR space | higher better |
| R1 / R2 / R3 | `test/tmr/R1`, `R2`, `R3` | generated TMR motion embedding vs TMR text embedding | text-to-motion retrieval: sort pairwise text-motion distances and check whether matched sample is within top k | higher better |
| TMR multimodal distance | `test/tmr/mm_distance` | generated TMR motion embedding vs TMR text embedding | mean diagonal distance between matched text and generated motion in retrieval matrix | lower better |

Important interpretation:

- FDTMR / HCov evaluate distribution and manifold coverage in learned human-text/motion latent space.
- TMR score and R@K evaluate text-motion alignment in the same learned space.
- These are not raw joint MSE. A visually plausible reconstruction can still score badly if TMR embedding is sensitive to distribution, normalization, or text-alignment mismatch.

### 2.1 Paired Human geometry 与 integrated-yaw diagnostics

StoryMotion 的 `paired_geometry` 是 reference-paired 诊断，不是 one-to-many 文本生成
的独立 hard gate。它在每个 sample 的 valid frames 上计算：

| output key | computation | unit / direction |
| --- | --- | --- |
| `human_global_mpjpe` | generated 与 reference 的世界坐标关节欧氏距离，对 frame/joint 取均值 | meter；lower |
| `human_root_aligned_mpjpe` | 每帧分别减去各自 pelvis 后的关节距离；只移除平移，不移除 heading | meter；lower |
| `human_root_ade` | generated/reference pelvis 逐帧距离均值 | meter；lower |
| `human_root_fde` | 最后一个 valid frame 的 pelvis 距离 | meter；lower |
| `human_integrated_yaw_geodesic_deg` | Human199 dim-3 经训练 mean/std 反归一化后分别 `cumsum`；预测与 reference 的 wrapped 角差绝对值对 valid frames 取均值 | degree；lower |
| `human_integrated_yaw_final_geodesic_deg` | 上述 wrapped 角差在最后一个 valid frame 的绝对值 | degree；lower |
| `human_integrated_yaw_final_unwrapped_error_deg` | 未 wrap 的累计角差在最后一个 valid frame 的绝对值；保留多圈 drift | degree；lower |

固定 heading strata 使用 reference Human199：

- `gt_net_yaw_deg`：累计 dim-3 后最后一帧绝对角度，bins 为
  `0–15/15–45/45–90/90+`；
- `gt_yaw_total_variation_deg`：逐帧 yaw increment 绝对值之和，bins 为
  `0–30/30–90/90–180/180+`；
- `gt_turn_reversals`：忽略绝对值不超过 `1e-4` 的 increment 后，符号改变次数，
  bins 为 `0/1/2+`。

这些值衡量完整 sampler 输出的累计 heading 误差。它们不能替代固定
`t=799` 的 teacher-forced single-step attribution，也不能把
root-aligned MPJPE 攵称为 yaw-aligned local-pose error。

## 3. Camera / CLaTr Metrics

PulpMotion implementation:

```text
linked/PulpMotion/src/callbacks/camera_metrics.py
linked/PulpMotion/src/metrics/encoders/clatr.py
linked/PulpMotion/src/metrics/frechet.py
linked/PulpMotion/src/metrics/prdc.py
linked/PulpMotion/src/metrics/similarity.py
linked/PulpMotion/src/metrics/retrieval.py
linked/PulpMotion/src/metrics/segment.py
```

Camera raw preprocessing:

1. Take raw camera poses `B x T x 4 x 4`.
2. Convert from PulpMotion coordinates to ET-v1 / RealEstate coordinates by a fixed matrix.
3. Translation feature is first-frame origin plus frame-to-frame velocity.
4. Normalize origin and velocity by CLaTr stats.
5. Convert rotation matrix to 6D rotation.
6. Concatenate rotation 6D and normalized translation to `B x T x 9`.
7. Encode generated camera trajectory, reference camera trajectory, and camera text into 256-d CLaTr latent vectors.

| display name | output key | input pair | computation | direction |
| --- | --- | --- | --- | --- |
| FDCLaTr | `test/clatr/fcd` | generated CLaTr trajectory embeddings vs reference CLaTr trajectory embeddings | Frechet distance between Gaussian fits in CLaTr latent space | lower better |
| CLaTr | `test/clatr/clatr_score` | generated CLaTr trajectory embedding vs CLaTr text embedding | cosine similarity, scaled by `100`, clamped at zero | higher better |
| CCov | `test/clatr/coverage` | generated vs reference CLaTr trajectory embeddings | PRDC coverage in CLaTr space, `k=3`, averaged over 5 chunks | higher better |
| CLaTr precision | `test/clatr/precision` | generated vs reference CLaTr trajectory embeddings | PRDC precision in CLaTr space | higher better |
| CLaTr recall | `test/clatr/recall` | generated vs reference CLaTr trajectory embeddings | PRDC recall in CLaTr space | higher better |
| CLaTr density | `test/clatr/density` | generated vs reference CLaTr trajectory embeddings | PRDC density in CLaTr space | higher better |
| CLaTr R1 / R2 / R3 | `test/clatr/R1`, `R2`, `R3` | generated CLaTr trajectory embedding vs CLaTr text embedding | text-to-camera retrieval | higher better |
| CLaTr multimodal distance | `test/clatr/mm_distance` | generated CLaTr trajectory embedding vs CLaTr text embedding | mean matched text-camera distance | lower better |

## 4. Camera Caption Segment Metrics

PulpMotion implementation:

```text
linked/PulpMotion/src/metrics/segment.py
```

Segment metric inputs:

| input | source | meaning |
| --- | --- | --- |
| raw predicted camera poses | `outputs["raw_output"]` for camera task | generated camera trajectory |
| raw labels | `batch["camera_segments"]` | per-frame camera movement class labels |
| mask | `batch["padding_mask"]` | valid frames |

Computation:

1. For each sample, keep valid trajectory frames.
2. Compute camera dynamics from pose sequence at `25 fps`.
3. Segment trajectory using translation velocity, xy/xz/yz velocity cues.
4. Smooth with window size `56`.
5. Remove short chunks smaller than `25` frames.
6. Compare predicted segment labels to target labels with weighted multiclass precision, recall, and F1.

| display name | output key | computation | direction |
| --- | --- | --- | --- |
| Caption precision | `test/captions/precision` | weighted multiclass precision between predicted and target camera segments | higher better |
| Caption recall | `test/captions/recall` | weighted multiclass recall between predicted and target camera segments | higher better |
| F1 | `test/captions/fscore` | weighted multiclass F1 between predicted and target camera segments | higher better |

Interpretation:

- In StoryMotion tables, `F1` means this camera-segment F1, not human action F1.
- It can improve while Out / TMR worsens because it only checks camera movement class segmentation.

## 5. Joint Projection Metrics

PulpMotion implementation:

```text
linked/PulpMotion/src/callbacks/joint_metrics.py
linked/PulpMotion/src/metrics/projection.py
linked/PulpMotion/src/metrics/frechet.py
```

Joint projection preprocessing:

1. Select 9 joints: pelvis, spine2, left ankle, right ankle, head, left shoulder, right shoulder, left wrist, right wrist.
2. Project generated 3D joints through generated camera poses and intrinsics.
3. Normalize image coordinates around the camera center:
   - x: `(pixel_x - cx) / cx`
   - y: `(cy - pixel_y) / cy`
4. Clamp normalized values to `[-2, 2]`.
5. Flatten 9 xy pairs to an 18D projection feature.

| display name | output key | input pair | computation | direction |
| --- | --- | --- | --- | --- |
| projection r_fpd | `test/proj/r_fpd` | generated-by-reprojection projection features vs GT `proj_joints` | Frechet distance over 18D projected joint features | lower better |
| projection g_fpd | `test/proj/g_fpd` | direct generated projection features vs GT `proj_joints` | Frechet distance; only meaningful when model outputs `x_output["projection"]` | lower better |
| projection error | `test/proj/error` | direct generated projection vs reprojection | MSE between generated projection branch and reprojected human/camera output | lower better |
| Out | `test/proj/outscreen` | generated-by-reprojection projection features | fraction of valid frames where fewer than `min_visible_joints=1` selected joint is inside normalized screen range `[-1, 1]` in both x and y | lower better |
| projection precision / recall / density / coverage | `test/proj/precision`, etc. | disabled in current callback | currently emitted as zeros because PRDC update is commented out | do not interpret |

Interpretation:

- Canonical generation tables report both `r_fpd` and `Out`；前者衡量投影分布，后者衡量逐帧 framing failure。
- `Out` is a per-frame visibility failure rate after projecting generated human through generated camera.
- `Out` can worsen even when camera CLaTr improves, because CLaTr judges trajectory/text latent alignment, while Out judges whether generated human stays visible in generated camera framing.

### 5.1 三种 `Out` 口径不得混用

StoryMotion当前有三个名称接近、输入和方向不同的projective字段：

| scope | machine key | input / reduction | interpretation |
| --- | --- | --- | --- |
| Stage2 generated system | `test/proj/outscreen` | generated Human + generated Camera；逐帧判断选定关节是否一个都不可见，再对valid frames取均值 | zero-visible frame failure rate；↓ |
| v10 Stage1 native diagnostic | `projective_outscreen` | GT Human + reconstructed Camera；先算每帧所有关节的出框fraction，再对valid frames取均值 | raw occupancy；描述性，**不是误差，不能默认↓** |
| canonical Stage1 paired reconstruction | `projective_out_ratio_abs_mean` | reconstructed Human/Camera与reference Human/Camera分别得到逐帧out-ratio，再取绝对差并按sequence等权汇总 | paired framing error；↓ |

因此，v10 native字段接近`0.5`只表示该cohort的构图中约一半关节处于画外；必须同时查看reference occupancy，不能把它写成“50% reconstruction error”。跨Stage1版本比较使用canonical paired字段；Stage2 generation表继续使用zero-visible failure `test/proj/outscreen`。审计数值只见 [[StoryMotion-valid-metric-ledger#6. Canonical Stage1 true-length paired reconstruction]]。

## 6. Decoded Human physical / kinematic diagnostics

StoryMotion implementation:

```text
linkedCodebases/StoryMotion/storymotion/per_sample_quality.py
```

输入是 owning decoder 输出的 raw skeleton joints，只保留每个样本的 valid
frames。每个字段先逐样本计算，再对 cohort 输出 `mean`、`median` 与 `p90`；
同一结果同时保存 generated 与 dataset-reference 汇总和逐样本 records。

| output key | computation | unit / direction |
| --- | --- | --- |
| `bone_length_cv_mean` | 21 条固定 skeleton bones 的逐帧 length CV，再对 bones 取均值 | dimensionless；lower 通常更稳定 |
| `joint_speed_mean` | 一阶 frame difference 的 joint-vector norm 均值 | decoded coordinate / frame；应与 reference 对照，不设单调方向 |
| `joint_acceleration_mean` | 二阶 frame difference 的 joint-vector norm 均值 | decoded coordinate / frame²；同上 |
| `joint_jerk_mean` | 三阶 frame difference 的 joint-vector norm 均值 | decoded coordinate / frame³；同上 |
| `root_speed_mean` | pelvis 一阶 frame difference norm 均值 | decoded coordinate / frame；应与 reference 对照 |
| `root_acceleration_mean` | pelvis 二阶 frame difference norm 均值 | decoded coordinate / frame²；应与 reference 对照 |
| `root_jerk_mean` | pelvis 三阶 frame difference norm 均值 | decoded coordinate / frame³；应与 reference 对照 |
| `foot_contact_rate_heuristic` | 双脚 z 不高于该 motion 自身脚高第 5 百分位加 `0.05` 的 frame fraction | fraction；应与 reference 对照 |
| `foot_skate_speed_heuristic` | 上述 contact frames 的双脚 frame-difference speed 均值 | decoded coordinate / frame；lower 通常更好 |

这些字段是 no-reference、未校准的 decoded diagnostic，不是独立 hard gate。
当前 generation evaluator 没有可信的统一地面平面，因此不输出 calibrated ground
penetration 或 floating；curation-only scorer 的 richer raw-GT 字段不能补入
generation table。

## 7. Current Stage1 / Stage2 training-objective I/O

> [!warning] Evidence boundary
> 本节固定“代码如何算 loss／TensorBoard tag 表示什么”，不把 loss 当成 decoded quality metric。具体 run 的 loss 数值、异常时间线与修复决策由 run artifact 和 [[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]] 拥有，不进入正式 metric ledger。

当前 v9 protected-H 实现入口：

```text
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/model.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/train.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual_pulp_only_r3/train.py
linkedCodebases/StoryMotion/storymotion/tokenizers/base.py
linkedCodebases/StoryMotion/experiments/stage2_backbone_upper_bound/e6_c3_vimogen_h/model.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/model.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/runner.py
```

### 7.1 Shared masked reductions

令 `M[b,t]` 为 valid-frame mask。Stage1 的 `masked_mean` 会把 `M` 扩展到
feature 维，然后只对所有 valid scalar 求均值；空 mask 返回 `0`。因此对于
`D` 维输入：

```text
masked_SmoothL1(P,Y,M)
  = sum_{b,t,d} M[b,t] SmoothL1(P-Y) / (D sum_{b,t} M[b,t])
```

`SmoothL1` 使用 PyTorch 默认 `beta=1`。一阶 temporal loss 使用相邻两帧都
valid 的 `M_delta[b,t] = M[b,t] and M[b,t-1]`：

```text
temporal_diff(P,Y,M)
  = masked_MSE(P[:,1:]-P[:,:-1], Y[:,1:]-Y[:,:-1], M_delta)
```

当前 v9 Stage1 objective 没有 acceleration 项；不要把旧 tokenizer family 的
acceleration 配置套到本实现。

### 7.2 Stage1 Human-anchor residual AE

输入是 normalized Human199 `H`、可选 official Camera14 `C` 与 raw-frame
mask；输出为 `H_hat`、可选 `C_hat`、framing prediction `F_hat`，以及
`z_h[128] + z_hc[16] + z_c[48]`。Human decoder 只读取 `z_h`；Camera 与
framing decoder 读取完整 joint latent。全路径显式 non-causal。

Human full-profile loss：

```text
L_H_recon = masked_SmoothL1(H_hat, H, M)
L_H_delta = temporal_diff(H_hat, H, M)
L_yaw     = masked_mean(1 - cos(yaw_hat - yaw), M)
L_root    = masked_SmoothL1(root_hat, root, M)

L_H = L_H_recon + L_H_delta + 0.001 L_yaw + 0.003 L_root
```

`yaw` 先把 Human199 dim `3` 按 Pulp train mean/std 反归一化，再沿时间
`cumsum`。`root` 使用同一 decoded yaw 把 local root XY velocity 旋转到 world
frame 后积分，并拼接 dim `0` 的 root height；所以 `L_yaw` 与 `L_root` 是
decoded cumulative diagnostics，不是 normalized channel MSE。

`root_local` profile只把 Human199 `[0:4]` 与 `[136:199]` 拼成 67D target来
计算 `L_H_recon` 和 `L_H_delta`；pose6D `[4:136]` 不受监督。`L_yaw`、
`L_root` 仍由 root/yaw channels计算。日志中的 `human_root_local_recon` 与
`human_pose_recon` 是分解项，不会再次加到 `L_H`；后者在 `root_local`
profile中为 `0`。

当前 completed Pulp-only run把同一 ordered Pulp cohort暴露为两个 role：
`pulp_anchor` 是 Camera-free `root_local` view，`pulp_joint` 是 full Human199 +
Camera14 view；没有 HumanML3D sample。早期 mixed-domain precursor曾把
`root_local` profile用于 HumanML3D，但那不是当前 Stage2 cache的 parent run。

Camera loss：

```text
L_C_recon = masked_SmoothL1(C_hat, C, M)
L_C_delta = temporal_diff(C_hat, C, M)
L_frame   = masked_SmoothL1(F_hat, F(H,C), M)
L_energy  = masked_mean(mean_channel(z_hc^2), M[:,::4])

L_C = L_C_recon + L_C_delta + 0.1 L_frame + 1e-4 L_energy
```

`F(H,C)` 从 GT Human 与 Camera 构造四维 detached target：归一化 screen
center xy、projected-joint bounding-box diagonal 的 `log1p`、以及几何出屏关节
比例。Camera14 relative-distance 会先反归一化，Human root 由上述 owning
decoder 语义恢复。`L_energy` 只正则 interaction16，不正则 camera48。

当前三阶段并非每步都同时算 `L_H + L_C`：

| Stage1 phase / role | steps / source cycle | current-step total | trainable route |
| --- | --- | --- | --- |
| A · `pulp_anchor` | `210K`；anchor : joint = `4:1` | `L_H(root_local)`；Camera输入移除 | Human encoder／decoder；Camera modules frozen |
| A · `pulp_joint` | 同上 | `L_H(full)`；Phase A仍移除 Camera输入 | Human encoder／decoder；Camera modules frozen |
| B · `pulp_joint` | `210K`；joint only | `L_C` | Human encoder／decoder frozen；Camera／interaction modules |
| C · `pulp_anchor` | `216K` 阶段内；anchor : joint = `3:7` | `L_H(root_local)`；`L_C=0` | Camera path不被调用、无 Camera gradient；Human LR `0.1x` |
| C · `pulp_joint` | 同上 | `L_H(full) + L_C` | Human LR `0.1x`；Camera LR `1x` |

Stage1 使用 FP32、batch `128`、AdamW、pre-clip threshold `1.0`。每阶段独立
linear warmup `1K`，随后从 base LR `5e-5` cosine 到 `1e-6`。

### 7.3 v10 Human-relative Camera Phase-B loss

v10从exact Phase-A `210K`加载并永久冻结`E_h,D_h`，只优化fresh `E_c,D_c`。输入Camera先经固定几何`Phi(H,C)`转换为Human-yaw-relative Camera14；输出经`Phi^-1`恢复world Camera。修正版loss为：

```text
L_rel_recon = masked_SmoothL1(C_rel_hat, C_rel, M)
L_rel_delta = temporal_diff(C_rel_hat, C_rel, M)
L_rot       = masked rotation geodesic(C_rel_hat, C_rel, M)

F(H,C) = concat(
  2 * (screen_center - 0.5),
  log1p(projected_joint_bbox_diagonal),
  soft_outscreen_ratio(softness=20.0)
)
L_frame = masked_SmoothL1(F(H,C_hat), stopgrad(F(H,C)), M)

L_C_v10 = L_rel_recon + L_rel_delta + 0.1 L_rot + 0.1 L_frame
```

`F`没有learned decoder；GT Human geometry与target feature均detach，故`L_frame`只向Camera encoder／decoder反传。`soft_outscreen_ratio`用sigmoid近似front与四条screen boundary，解决hard in/out boolean不可微的问题；正式报告仍使用hard occupancy、paired Out error与zero-visible三种独立口径，不用soft proxy冒充评测值。

v9 Phase C没有新增Camera loss：joint role仍使用与Phase B相同的`L_C`，只额外加入`L_H`并解冻Human。因此v10 Phase B迁移v9中合理且仍有owner的Camera recon、temporal与`0.1 framing`；不迁移已删除`interaction16`的energy项，也不迁移会改变冻结Human owner的Phase-C Human loss。v10额外保留`0.1 rotation geodesic`。

2026-07-29旧v10 `210K` run只训练`L_rel_recon + L_rel_delta + 0.1 L_rot`，没有`L_frame`反传。其数值是历史diagnostic，不是修正版cache候选；修正版trainer revision与contract hash均拒绝resume旧checkpoint／optimizer。

### 7.4 Stage2 shifted-flow loss

输入 `H_0` 为 whitened Human128，`C_0` 为 whitened Camera64，tensor shape
分别为 `[B,128,75]` 与 `[B,64,75]`。对每个 sample 独立采样
`u ~ Uniform(0,1)` 与 Gaussian noise `epsilon`：

```text
sigma   = 5u / (1 + 4u)
x_sigma = (1-sigma) x_0 + sigma epsilon
v_star  = epsilon - x_0

L_flow(D) = mean_b [
  sum_{d,t} M[b,t] (v_pred-v_star)^2
  / (D sum_t M[b,t])
]
```

分母先按每个 sample 的 valid latent frames 与 channel 数归一化，再对 batch
求均值；Human 使用 `D=128`，Camera 使用 `D=64`。这不是 SNR-weighted loss，
也没有 decoded Camera-center、rotation、framing、projection 或 outscreen 项。

| Stage2 route | predicted tensor | condition / target construction | current loss |
| --- | --- | --- | --- |
| Direct-H teacher | Human128 velocity | Human text；training condition dropout `0.1` | `L_H_flow(128)` |
| Camera given Human | Camera64 velocity | clean observed `H_0.detach()`；`observed_human=true`，所有 `sigma` 的 Human trust 为 `1` | `L_C_given_H_flow(64)` |
| joint-training `HC` | Camera64 velocity | 同一 `sigma` 下 noisy GT Human 经 frozen Human teacher 单次 conditional forward 得到 `H_tilde = H_sigma - sigma v_H`，再 detach；Camera 内部 trust 为 `(1-sigma)^1` | `L_HC_flow(64)` |

Camera training 时 frozen Human teacher 处于 eval mode，因此上表 `HC` context
forward 没有 Human-text dropout，也没有 CFG 放大；等价于 conditional scale
`1`。Camera branch 内的 Camera-text 与 Human-context row dropout 各为 `0.1`，
两者独立采样。

Human teacher 先独立训练 `105K` steps，随后 materialize Human EMA 并永久冻结。
Camera 的 `105K` steps 共用一个 Camera branch、AdamW state 与 EMA，而且每个
optimizer step **只优化一个 route loss**；代码没有 `L_C_given_H + L_HC` 的
同一步加权和：

| Camera phase step | global step | active route / scalar actually backpropagated |
| --- | --- | --- |
| `1–35K` | `105001–140K` | Camera given Human only |
| `35001–70K` | `140001–175K` | joint-training `HC` only |
| `70001–105K` odd | `175001–210K` odd global step | Camera given Human only |
| `70001–105K` even | `175001–210K` even global step | joint-training `HC` only |

已完成 v9 run 的 Human 与 Camera micro/effective batch 均为 `128/128`，gradient
accumulation 均为 `1`；Stage2 使用 BF16 autocast。两段各 `105K` optimizer
steps，因此 Camera 总 sample exposures 为 `13.44M`，但每个 Camera route 只有
`52.5K × 128 = 6.72M` exposures。

### 7.5 Optimizer and TensorBoard tag semantics

Stage2 两段各使用 AdamW：base LR `2e-4`、warmup `2K`、phase step `80K`
起乘 `0.1`、betas `(0.9,0.95)`、weight decay `0.01`、EMA `0.9999`。Camera
phase step `80K` 对应 global step `185000`；该步记录的 LR 已是 `2e-5`。

| TensorBoard tag | exact producer / interpretation |
| --- | --- |
| `loss/camera_train_C_H` | 当前非 EMA Camera branch 的 stochastic Camera-given-H loss；只有该 route active 时才写入 |
| `loss/camera_train_HC` | 当前非 EMA Camera branch 的 stochastic `HC` loss；只有该 route active 时才写入 |
| `loss/camera_eval_fixed_ema_C_H` | 每次 eval 都用相同 held-out loader／seed评估 Camera EMA 的 Camera-given-H loss，不受当前 active route 限制 |
| `loss/camera_eval_fixed_ema_HC` | 同上，但评估 `HC` context；与上一行一起判断 cross-route forgetting |
| `train/camera_grad_norm` | `clip_grad_norm_` 的返回值，即 threshold `1.0` **裁剪前**的 total norm；它不是裁剪后 norm |
| `train/camera_lr` | 当前 Camera phase step 实际写入 optimizer param group 的 LR |

因此 `loss/camera_train_C_H` 在 global `140001–175000` 没有点是 curriculum
明确不运行该 route，不是 event file 丢写。两个 train loss还各自混合了随机
batch、`sigma`、noise 与 condition dropout；判断遗忘应优先看同时计算的两条
fixed-EMA held-out curve。

## 8. Scope exclusions and routing

- 本页拥有归一化 feature-space objective 与 TensorBoard tag 的计算定义；具体数值只属于对应 run 的 contract、manifest、event file 或训练诊断页，不进入 metric ledger。
- 数据清洗的 raw-GT hygiene counters 只由 [[2026-07-17_storymotion-v8-2333-data-curation-plan]] 拥有，不用于生成系统排名。
- `START_X objective`、flow prediction target 等名称可以作为方法 provenance；它们不是 metric。

## 9. JSON Output Layout

Canonical Stage2 generation output:

```json
{
  "task": "human | camera | joint",
  "metric_task": "human | camera | joint",
  "run": {"checkpoint": "...", "checkpoint_sha256": "...", "is_causal": false},
  "sampler": {"name": "...", "num_steps": 50, "seed": 17},
  "metrics": {"test/tmr/ftd": "..."},
  "observed_human_projective": null,
  "paired_geometry": {"overall_mean": {}, "records": []},
  "decoded_human_physical": {"generated": {}, "dataset_reference": {}, "records": []},
  "records_path": "..."
}
```

Display-name mapping used in StoryMotion tables:

| table name | JSON key | source callback |
| --- | --- | --- |
| Human semantic/distribution | `metrics["test/tmr/*"]` | Direct-H / joint parallel |
| Camera semantic/distribution | `metrics["test/clatr/*"]` | Direct-C / joint parallel |
| Camera segment | `metrics["test/captions/*"]` | Direct-C / joint parallel |
| Joint projection | `metrics["test/proj/r_fpd"]`, `metrics["test/proj/outscreen"]` | joint parallel |
| observed-H projective | `observed_human_projective.metrics["test/proj/r_fpd"]`, `...outscreen` | Direct-C only |
| paired Human/Camera geometry | `paired_geometry.overall_mean.*` | applicable mode |
| decoded Human physical | `decoded_human_physical.generated.*` plus `dataset_reference.*` | Direct-H / joint parallel |

## 10. Practical Reading Rules

- Use Direct-H rows only for free Human generation claims.
- Use Direct-C rows for observed-Human Camera completion; its projective fields stay in that mode.
- Use joint-parallel rows when judging freely generated Human and Camera from the same checkpoint; joint rows include the complete Human, Camera, caption, projection, geometry, and applicable decoded-physical sets.
- Do not compare mixed `10549` rows directly against pure `4053` rows.
- Do not treat projection PRDC zeros as evidence; those metrics are disabled in `JointMetricCallback`.
- Treat F1 as camera segment F1, not full semantic action F1.
- Treat Out as framing/visibility failure, not a distributional embedding score.
