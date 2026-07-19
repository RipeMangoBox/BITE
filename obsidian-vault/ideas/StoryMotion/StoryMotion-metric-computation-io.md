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
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[archived/evidence/2026-07-11_storymotion-v7.14-corrected-results]]"
  - "[[archived/evidence/2026-07-12_storymotion-v7.17-decoder-cache-contract-execution]]"
created: 2026-07-09T12:20:00+0800
updated: 2026-07-18T14:11:00+08:00
---

# StoryMotion Metric Computation IO

> [!abstract] Scope
> 本页说明 StoryMotion 当前文档里出现的 metric 如何计算、吃什么输入、输出什么键。核心 official 指标来自 PulpMotion official callback；StoryMotion 本地脚本只负责把 Stage1 / Stage2 输出转成 PulpMotion callback 期望的 `raw_input`、`raw_output`、`x_output` 和 batch 字段。Feature-space MSE / loss 只作 debug，不进入正式 ranking。

## 1. Evaluation Data Contract

Stage1 official reconstruction eval 入口：

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_joint_tokenizer_official_recon.py
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
- Reconstructed human features are decoded to official human raw joints by `feature_dataset.human_dataset.get_raw`.
- Reconstructed camera features are converted from StoryMotion camera features to camera poses by `camera_features_to_poses`.
- Official callbacks then run unchanged.

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

- StoryMotion tables usually report `Out` but not `r_fpd`.
- `Out` is a per-frame visibility failure rate after projecting generated human through generated camera.
- `Out` can worsen even when camera CLaTr improves, because CLaTr judges trajectory/text latent alignment, while Out judges whether generated human stays visible in generated camera framing.

## 6. Posthoc Feature-Space Metrics

StoryMotion local implementation:

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_joint_separate_tokenizers_posthoc.py
linkedCodebases/StoryMotion/storymotion/eval/metrics.py
linkedCodebases/StoryMotion/storymotion/training/joint_trainer.py
```

These are not official PulpMotion metrics. They compare normalized tokenizer feature tensors before raw decode / official callbacks.

| output key | input | computation | use |
| --- | --- | --- | --- |
| `metric_human_mse` | `human_recon`, `human`, valid mask | mean squared feature error over valid frames | debug only |
| `metric_human_mae` | same | mean absolute feature error over valid frames | debug only |
| `metric_camera_mse` | `camera_recon`, `camera`, valid mask | mean squared camera-feature error over valid frames | debug only |
| `metric_camera_mae` | same | mean absolute camera-feature error over valid frames | debug only |
| `metric_human_frame_l2` | human feature diff | per-frame L2 norm, averaged over valid frames | debug only |
| `metric_camera_frame_l2` | camera feature diff | per-frame L2 norm, averaged over valid frames | debug only |
| `metric_human_root_mse` | first 4 human feature dims | MSE over root-like feature prefix | debug only |
| `metric_human_velocity_mse` | frame differences | MSE of first-order human feature differences on adjacent valid frames | debug only |
| `metric_camera_velocity_mse` | frame differences | MSE of first-order camera feature differences on adjacent valid frames | debug only |
| `mpjfe` | generic recon/target tensor | mean per-frame feature L2 | debug only |
| `max_frame_error` | generic recon/target tensor | max per-frame feature L2 | debug only |
| `root_mse` | first up-to-3 dims | root-prefix MSE | debug only |
| `velocity_mse` | adjacent frame differences | MSE of feature velocity error | debug only |

Rule:

- Do not rank official model quality by these values.
- They are useful for diagnosing whether a tokenizer reconstructs its normalized input features, but they do not substitute for TMR / CLaTr / projection callbacks.

## 7. Training Loss Metrics

Stage1 tokenizer training loss implementation:

```text
linkedCodebases/StoryMotion/storymotion/tokenizers/base.py
linkedCodebases/StoryMotion/storymotion/tokenizers/joint_human_camera.py
linkedCodebases/StoryMotion/scripts/train_storymotion_joint_tokenizer.py
```

Loss inputs:

| tensor | shape | meaning |
| --- | --- | --- |
| `human` | `B x T x D_h` | normalized human feature target |
| `camera` | `B x T x D_c` | normalized camera feature target |
| `human_recon` | `B x T x D_h` | tokenizer reconstruction |
| `camera_recon` | `B x T x D_c` | tokenizer reconstruction |
| `mask` | `B x T` | valid frames |

Loss terms:

| key | computation |
| --- | --- |
| `human_recon_loss` | masked SmoothL1 between `human_recon` and `human` |
| `camera_recon_loss` | masked SmoothL1 between `camera_recon` and `camera` |
| `human_velocity_loss` | MSE between adjacent-frame differences of human recon and target |
| `camera_velocity_loss` | MSE between adjacent-frame differences of camera recon and target |
| `human_acceleration_loss` | MSE between second-order temporal differences of human recon and target |
| `camera_acceleration_loss` | MSE between second-order temporal differences of camera recon and target |
| `commitment_loss` | quantizer commitment loss when tokenizer uses VQ / FSQ style quantization |
| `total_loss` | weighted sum of reconstruction, velocity, acceleration, and commitment terms |

Default v7.12 separate tokenizer settings:

| tokenizer family | default `velocity_weight` | effective human velocity | effective camera velocity | acceleration |
| --- | ---: | ---: | ---: | ---: |
| separate AE | 1.0 | 1.0 | 1.0 | 0 |
| separate VAE | 1.0 | 1.0 | 1.0 | 0 |
| separate GRFSQ | 0.5 | 0.5 | 0.5 | 0 |

Human-stronger v1 settings:

```yaml
human_recon_weight: 2.0
camera_recon_weight: 1.0
human_velocity_weight: 1.0
camera_velocity_weight: 0.25
human_acceleration_weight: 0.25
camera_acceleration_weight: 0.05
```

Rule:

- Loss tables should stay out of the formal metric ledger.
- Loss is a training/debug signal in normalized feature space, while official metrics evaluate decoded raw human / camera outputs.

## 8. Clean-Filter Diagnostic Metrics

Clean filter implementation:

```text
linkedCodebases/StoryMotion/scripts/storymotion_v75_clean_filter.py
```

These metrics classify obvious-bad GT samples for hygiene filtering, not model quality.

| key | input | computation | use |
| --- | --- | --- | --- |
| `root_disp` | decoded root trajectory | distance between first and last root position | severe drift / stationary contradiction |
| `root_path` | decoded root trajectory | sum of frame-to-frame root displacement | excessive motion path |
| `xy_span` | decoded root trajectory | xy bounding-box span | lateral/global drift |
| `z_span` | decoded root trajectory | vertical range | unsupported vertical outlier |
| `max_step` | decoded root trajectory | max adjacent-frame root step | discontinuity / jump artifact |

## 9. JSON Output Layout

Official Stage1 reconstruction output:

```json
{
  "mode": "storymotion_stage1_tokenizer_reconstruction_official_metrics",
  "set_name": "pure_",
  "split": "test",
  "evaluated_samples": 4053,
  "model": {"name": "...", "preset": "...", "checkpoint": "..."},
  "metric_results": {
    "human": {"metrics": {"test/tmr/ftd": 0.0}},
    "camera": {"metrics": {"test/clatr/fcd": 0.0}},
    "joint": {"metrics": {"test/tmr/ftd": 0.0, "test/clatr/fcd": 0.0, "test/proj/outscreen": 0.0}}
  },
  "records_path": "..."
}
```

Display-name mapping used in StoryMotion tables:

| table name | JSON key | source callback |
| --- | --- | --- |
| FDTMR | `metric_results.*.metrics["test/tmr/ftd"]` | human / joint |
| TMR | `metric_results.*.metrics["test/tmr/tmr_score"]` | human / joint |
| HCov | `metric_results.*.metrics["test/tmr/coverage"]` | human / joint |
| FDCLaTr | `metric_results.*.metrics["test/clatr/fcd"]` | camera / joint |
| CLaTr | `metric_results.*.metrics["test/clatr/clatr_score"]` | camera / joint |
| CCov | `metric_results.*.metrics["test/clatr/coverage"]` | camera / joint |
| F1 | `metric_results.*.metrics["test/captions/fscore"]` | camera / joint |
| Out | `metric_results.*.metrics["test/proj/outscreen"]` | joint only |

## 10. Practical Reading Rules

- Use human-task rows for human-only reconstruction/generation claims.
- Use camera-task rows for camera-only reconstruction/generation claims.
- Use joint-task rows when judging paired human-camera output; joint rows include human TMR, camera CLaTr / caption, and projection Out.
- Do not compare mixed `10549` rows directly against pure `4053` rows.
- Do not treat projection PRDC zeros as evidence; those metrics are disabled in `JointMetricCallback`.
- Treat F1 as camera segment F1, not full semantic action F1.
- Treat Out as framing/visibility failure, not a distributional embedding score.
