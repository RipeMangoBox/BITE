---
hypothesis: "StoryMotion 使用冻结的 PulpMotion Stage1 作为连续 human/camera latent tokenizer，并用 branch-mask continuous inpainting diffusion 在一个 Stage2 模型内统一支持 camera completion、human completion 与 joint generation。基于 official full-test evaluator，当前已验证的最佳均衡设置在 mixed joint generation 上显著改善 camera-human geometry、FDTMR 与 coverage；但不支配所有 PulpMotion Aux/MAR semantic 指标，human motion/contact 质量仍需独立 raw-skeleton gate 才能形成正式感知质量结论。"
status: in_progress
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
created: 2026-06-16T14:30:00+08:00
updated: 2026-06-17T16:45:00+08:00
supersedes: "[[2026-06-13_storymotion-v2-branchmask-inpainting]]"
---

# StoryMotion V3：正式全量测试记录

> [!abstract] 核心结论
> StoryMotion V3 记录当前正式版本的 branch-mask continuous inpainting 方案。本文只保留 official full-test 上可比较的结果。
>
> PulpMotion paper 中 16 个 `(x,y)` / `(x,y,z)`、Aux / no-Aux、DiT / MAR、pure / mixed setting 已完成 5090 full-test audit：其中 14 个 setting 可用官方 checkpoint、config、sampler 与 evaluator 直接复跑；DiT `(x,y,z) Aux` 的 mixed 与 pure 两行需要在 5090 本地 PulpMotion 修复 Standard CFG 维度对齐 bug 后才能复跑，因此单独标记为 local bugfix rerun。
>
> 当前 StoryMotion 正式设置为 independent-modality-dropout fine-tuning + 50-step DDIM START_X sampler，`cfg=2.0`，`eta=1.0`。在 mixed full test 上，该设置达到 FDframing=0.535、Out-rate=7.89%、FDTMR=155.73、TMR-Score=23.95、FDCLaTr=85.70、CLaTr-Score=33.52、F1=37.40%、Human Coverage=36.43%、Camera Coverage=62.83%。相对本次 5090 PulpMotion mixed full rerun，StoryMotion 的优势主要集中在 geometry、FDTMR、Human Coverage 与 Camera Coverage；TMR-Score、FDCLaTr、CLaTr-Score 与 F1 不支配所有 PulpMotion Aux/MAR setting。
>
> 2026-06-17 下午新增 Stage1 autoencoder upper-bound probe、human completion dependency probe 与 PulpMotion native camera projection render。已完成证据显示：pure split Stage1 reconstruction upper bound 明显强于 Stage2 generation；human completion 对 camera text zero / shuffle 都几乎不敏感，但对 observed camera latent zero / shuffle 明显敏感。Stage1 mixed full、text zero-human / shuffle-human / zero-all 与 camera latent noise full metric 仍在 5090 上运行，未写入完成结论。
>
> 2026-06-17T16:33+08:00，5090 `/data` 所在 `/dev/sda` 确认为介质级读错误并触发 ext4 inode table 读失败；StoryMotion 实验已停止，完成 JSON 与 partial records 已救援到 SSD 和本地。详见 [[2026-06-17_storymotion-5090-sda-failure-rescue]]。
>
> 渲染层面只引用 `linkedCodebases/StoryMotion/runs/eval/stage2/` 下的 corrected fair-compare 包；`linkedCodebases/StoryMotion/stage2/` 已于 2026-06-17 用正确 `runs/eval/stage2/` 镜像硬替换，旧错误 skeleton/renders 不再作为证据。

---

## 1. 正式主张

StoryMotion 用一个 Stage2 模型覆盖三种 human-camera generation mode：

| 模式 | 输入条件 | 生成分支 | 评估定位 |
| --- | --- | --- | --- |
| Camera completion | text + human latent | camera latent | StoryMotion 内部 completion 能力 |
| Human completion | text + camera latent | human latent | StoryMotion 内部 completion 能力 |
| Joint generation | text only | human + camera latent | 与 PulpMotion text-to-joint baseline 公平对比 |

核心主张：

1. PulpMotion frozen continuous human/camera tokenizer 可以作为统一 latent space，支持单一 branch-mask diffusion 模型覆盖三种任务。
2. 在相同 mixed test split 与 Pulp official callbacks 下，StoryMotion 当前均衡设置显著改善 camera-human geometry、FDTMR 与 coverage；完整 PulpMotion matrix 后不声明支配所有 semantic 指标。
3. Completion modes 是 StoryMotion 的额外能力，应单独报告；它们不是 PulpMotion text-only joint generation 的直接替代任务。
4. Human motion 的视觉质量、接触质量和骨架动力学需要 skeleton-space gate 单独验证，不能只由 aggregate evaluator 指标推出。

---

## 2. 方法

### 2.1 Frozen Continuous Tokenizer

StoryMotion 复用 PulpMotion Stage1 作为冻结连续 tokenizer：

```text
z = concat([z_hum, z_cam]) ∈ R^{192 × T}
z_hum ∈ R^{128 × T}
z_cam ∈ R^{64 × T}
```

Camera branch 表示 subject-relative camera state，包括 framing distance、FOV 相关量与 pose dynamics。

### 2.2 Branch-Mask Continuous Inpainting

Stage2 是作用于连续 latent sequence 的 DiT-style diffusion model。不同任务通过 branch mask 指定 observed branch 与 target branch。

| 任务                | Observed branch | Target branch  |
| ----------------- | --------------- | -------------- |
| Camera completion | human           | camera         |
| Human completion  | camera          | human          |
| Joint generation  | none            | human + camera |

当前正式设置使用 START_X prediction、50-step DDIM sampling、text classifier-free guidance、`cfg=2.0` 与 `eta=1.0`。

### 2.3 当前验证配置

当前 full-test 已验证 checkpoint 使用 independent modality text dropout fine-tuning。该配置增强了模型与 classifier-free guidance 的兼容性，并在 joint 与 completion mode 上保持一致的可用性。

当前长训练候选已完成 5090 full official probe 与 corrected raw-skeleton render gate，但不替代正式 checkpoint。GPU1 stable best 在 geometry、FDCLaTr 与 camera completion 上更强，但 joint TMR-Score 低于当前正式 checkpoint；GPU3 risky best 的 joint TMR-Score 更高，但 geometry、Out-rate 与 raw-skeleton contact gate 更弱。22:42 CST 的早期 joint 作业误用 evaluator 默认 `run_dir/last.pt`，已停止并移入 `v3_closure_20260616/obsolete_lastpt_partial/`，不进入结论。

### 2.4 Stage1 / Stage2 Loss 口径

| 阶段 | 训练目标 | loss 口径 | 已审计源码 / 配置 |
| --- | --- | --- | --- |
| PulpMotion Stage1 autoencoder | 把 official multimodal feature 编码到 continuous latent，再 decode 回 feature/raw motion | 本文不重述 autoencoder 训练 loss；当前只把 frozen official checkpoint 当作 reconstruction upper-bound evaluator 使用 | `scripts/eval_stage1_pulp_autoencoder_official.py` 调用 `cfg.model.autoencoder.load_checkpoint()`；full metric 证据见 `stage1/official_upper_bound_20260617/` |
| PulpMotion generation baseline | text-to-motion diffusion noise prediction | `SplitDDPMLoss` 对 camera、projection、human 三个分支分别计算 predicted noise MSE，并用 `loss_weights: [1.0, 1.0, 1.0]` 加权求和 | `linked/PulpMotion/src/models/generation/losses/ddpm.py`；`linked/PulpMotion/configs/model/loss/split_ddpm.yaml` |
| StoryMotion Stage2 | CondMDI-style branch-mask continuous inpainting diffusion | START_X prediction；只在 target branch 与 valid latent frames 上计算 per-sample MSE，observed branch 排除；当前正式 checkpoint 使用 `joint_loss_mode=element_mean` | `scripts/train_stage2_condmdi_pulp.py` 的 `make_branch_masks`、`masked_target_mse`、`diffusion_loss`；run meta 记录 `loss: per-sample MSE over target branch and valid latent frames only; observed branch excluded` |

StoryMotion 当前 independent-dropout fine-tune 的 meta：latent order 为 `concat([z_hum,z_cam])`，human slice `[0,128]`，camera slice `[128,192]`，`cond_mask_prob=0.0`，`cond_mask_prob_cam=0.1`，`cond_mask_prob_hum=0.1`，task probabilities 为 `[1.0,1.0,1.0]`，cosine diffusion 1000 training steps，resume 自 branchmean/jointheavy checkpoint。

---

## 3. 评估协议

StoryMotion 正式横向比较使用 10549-sample mixed full test。PulpMotion official matrix 额外包含 4053-sample pure full test，用于补齐 paper Table 8 对照与 official support audit；pure 行不与 StoryMotion mixed 行作直接公平优劣判断。

```text
StoryMotion sampler
  -> latent sequence
  -> PulpMotion frozen autoencoder.decode
  -> dataset.get_raw
  -> Pulp official metric callbacks
```

指标解释：

| 指标组                                                  | 含义                                   | 正式用途                                |
| ---------------------------------------------------- | ------------------------------------ | ----------------------------------- |
| FDframing ↓ / Out-rate ↓                             | projected camera-human geometry      | camera-human geometry comparison    |
| FDTMR ↓ / TMR-Score ↑ / R3 ↑ / Human Coverage ↑      | human-motion semantic distribution   | human-side aggregate comparison     |
| FDCLaTr ↓ / CLaTr-Score ↑ / F1 ↑ / Camera Coverage ↑ | camera-caption semantic distribution | camera-side aggregate comparison    |
| Raw-skeleton dynamics/contact                        | decoded joint motion quality         | checkpoint selection gate；尚不作为优越性结论 |

逐指标解释：

| 指标                                           | 越高/越低越好                                  | 独立含义                                                                                                          | 解释注意事项                                                                                               |
| -------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| FDframing                                    | 越低越好                                     | 生成的 human-camera 投影关系与参考分布之间的 Fréchet distance；主要衡量 framing geometry 的分布接近程度                                  | 低 FDframing 说明相机与人体几何关系更接近数据分布，但不能单独证明人体动作自然                                                         |
| Out-rate                                     | 越低越好                                     | 人体投影落出有效画面或 framing 约束失败的比例                                                                                   | 是 camera-human composition 的失败率指标，不等价于 semantic alignment                                            |
| FDTMR                                        | 越低越好                                     | TMR feature 空间中 generated human motion distribution 与 reference human motion distribution 的 Fréchet distance  | 更偏 distribution-level human motion 质量；不直接衡量单个 caption 是否被正确执行                                        |
| TMR-Score                                    | 越高越好                                     | TMR encoder 下 human motion 与文本 caption 的检索/匹配分数                                                               | 更贴近 text-only human-caption alignment；conditional completion 中低分可能混合 evaluator-task mismatch 与真实语义退化 |
| R1 / R2 / R3                                 | 越高越好                                     | human 或 camera caption retrieval 的 top-k 命中率，表示正确文本/运动是否排在前 k                                                 | 依赖 evaluator retrieval protocol；不同 table 中的 R3 口径需与 official callback 输出保持一致                         |
| Human Coverage                               | 越高越好                                     | generated human motion 在 TMR manifold 中覆盖 reference distribution 的比例                                          | 高 coverage 表示多样性/覆盖范围强，但可能伴随 precision 或 text alignment 下降                                           |
| FDCLaTr                                      | 越低越好                                     | CLaTr feature 空间中 generated camera trajectory distribution 与 reference camera distribution 的 Fréchet distance | 主要衡量 camera-side distribution，不说明 human skeleton 动作质量                                                |
| CLaTr-Score                                  | 越高越好                                     | CLaTr encoder 下 camera trajectory 与 camera caption 的匹配分数                                                      | 是 camera-caption semantic 指标；不能替代 projection render 或 Out-rate                                       |
| F1                                           | 越高越好                                     | camera segment / camera-event 类指标的综合 F1                                                                       | 对 camera motion event 或 caption segment 更敏感；不能单独解释整体 cinematic quality                               |
| Camera Coverage                              | 越高越好                                     | generated camera trajectory 在 CLaTr manifold 中覆盖 reference distribution 的比例                                   | 高 coverage 表示 camera 分布覆盖强，但需要结合 FDCLaTr、CLaTr-Score 与 render 检查可用性                                  |
| PRDC precision / recall / density / coverage | precision、recall、density、coverage 越高通常越好 | 在 TMR/CLaTr feature manifold 上衡量 generated distribution 与 reference distribution 的局部邻域关系                      | 作为 distribution diagnostic 使用；不能替代 sample-level 视觉验证                                                 |
| Raw-skeleton MPJPE                           | 越低越好                                     | decoded raw skeleton 与 GT skeleton 的 root-aligned joint error                                                 | 当前只用于小样本 render gate；不作为 full-set official superiority claim                                         |
| Contact proxy diff                           | 越低越好                                     | 生成动作与参考动作的 foot/contact proxy 差异                                                                              | 是 contact/dynamics diagnostic；可能与 MPJPE 存在 tradeoff，需要和视频一起解释                                        |

指标来源与口径：

| 指标 | 来源组件 | 计算对象 | 本文解释边界 |
| --- | --- | --- | --- |
| FDframing / Out-rate | PulpMotion joint projection callback | decoded human joints + camera + intrinsics 的投影关系 | 只说明 camera-human geometry，不等价于 human perceptual quality |
| FDTMR / TMR-Score / R1-R3 / Human Coverage | PulpMotion HumanMetricCallback / TMR encoder | decoded human motion 与 caption embedding / reference motion distribution | TMR retrieval 更贴近 text-only full motion-caption 对齐；conditional completion 下需谨慎解释 |
| FDCLaTr / CLaTr-Score / R1-R3 / Camera Coverage / F1 | PulpMotion CameraMetricCallback / CLaTr encoder + segment metrics | decoded camera trajectory 与 camera caption / reference distribution | camera-side semantic aggregate，不单独证明 human motion 质量 |
| PRDC coverage / precision / recall / density | PulpMotion ManifoldMetrics | TMR/CLaTr feature manifold | 作为分布覆盖/密度证据，不能替代 sample-level render gate |
| Raw-skeleton MPJPE/contact proxy | StoryMotion corrected fair-compare render summary | decoded raw skeleton sample diagnostics | 仅是 2-sample gate，不能作总体优越性结论 |

Joint generation 与 PulpMotion text-only joint generation setting 比较，因为两者都是 text-only 生成人体与相机运动。Completion modes 因为额外给定 observed branch，只作为 StoryMotion 内部能力报告。

渲染证据采用 corrected fair-compare render path：

```text
StoryMotion sampler / PulpMotion official sampler
  -> PulpMotion frozen autoencoder.decode
  -> dataset.get_raw
  -> corrected 3D skeleton renderer + shared render context
```

有效渲染包位于 `linkedCodebases/StoryMotion/runs/eval/stage2/`，尤其是 `joint_channel_gated_pulpmotion_fair_compare_20260615/`、`gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616/`、`v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare/` 与 `v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare/`。这些包的 `manifest.json`、每个 config 的 `render_summary.json`、每个 sample 的 `summary.json` 记录了 checkpoint、sample IDs、PulpMotion baselines、concat MP4、`fair_compare.png` 与 raw-joint motion statistics。旧的 `linkedCodebases/StoryMotion/stage2/` 已替换为正确镜像；替换前的 skeleton 图不进入 V3 结论。

---

## 4. Full-Test 结果

### 4.1 核心对比总表

所有 PulpMotion 行均使用官方 checkpoint、官方 config、50-step sampler 与 official metric callbacks；StoryMotion 行使用相同 mixed full test split 与 official callbacks。FDframing、Out-rate、FDTMR、FDCLaTr 越低越好，其余指标越高越好。

| model                                           | pure or mixed | FDframing ↓ | Out-rate ↓ | FDTMR ↓ | TMR-Score ↑ |  R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| ----------------------------------------------- | ------------- | ----------: | ---------: | ------: | ----------: | ----: | ---------------: | --------: | ------------: | -----: | ----------------: |
| PulpMotion DiT (x,y) no-Aux                     | mixed         |       5.148 |     26.59% |  377.36 |       23.36 | 11.58 |           10.43% |     88.42 |         31.31 | 35.05% |            50.49% |
| `PulpMotion DiT (x,y) Aux`                      | mixed         |       3.777 |     17.35% |  428.53 |       24.97 | 12.42 |            8.55% |     82.19 |         33.28 | 36.67% |            48.09% |
| PulpMotion DiT (x,y,z) no-Aux                   | mixed         |       7.242 |     35.98% |  440.91 |       24.21 | 18.95 |            7.68% |    106.77 |         25.29 | 28.36% |            48.11% |
| `PulpMotion DiT (x,y,z) Aux` local bugfix rerun | mixed         |       5.872 |     24.81% |  519.55 |       25.56 | 19.77 |            6.18% |    114.18 |         26.16 | 28.65% |            42.78% |
| PulpMotion MAR (x,y) no-Aux                     | mixed         |       8.122 |     42.92% |  277.38 |       20.71 | 16.49 |           19.98% |    125.47 |         38.22 | 39.29% |            54.67% |
| `PulpMotion MAR (x,y) Aux`                      | mixed         |       6.399 |     36.18% |  296.96 |       23.53 | 17.06 |           16.15% |    113.97 |         41.94 | 42.23% |            55.10% |
| PulpMotion MAR (x,y,z) no-Aux                   | mixed         |       9.608 |     42.34% |  276.66 |       19.07 | 26.18 |           20.47% |    153.61 |         36.86 | 36.57% |            50.65% |
| `PulpMotion MAR (x,y,z) Aux`                    | mixed         |       7.392 |     34.21% |  285.07 |       21.82 | 27.32 |           17.51% |    149.33 |         39.67 | 38.96% |            48.72% |
| PulpMotion DiT (x,y) no-Aux                     | pure          |       7.404 |     39.54% |  375.01 |       20.53 | 10.29 |           14.90% |     94.84 |         35.69 | 49.05% |            48.33% |
| PulpMotion DiT (x,y) Aux                        | pure          |       5.893 |     28.47% |  414.80 |       21.66 | 10.54 |           13.82% |     93.27 |         37.78 | 51.27% |            44.81% |
| PulpMotion DiT (x,y,z) no-Aux                   | pure          |       9.871 |     46.35% |  405.26 |       20.52 |  9.38 |           13.08% |     92.75 |         33.35 | 45.99% |            52.23% |
| `PulpMotion DiT (x,y,z) Aux` local bugfix rerun | pure          |       7.285 |     35.41% |  435.10 |       21.93 | 17.44 |           12.71% |     86.20 |         35.53 | 49.49% |            49.10% |
| PulpMotion MAR (x,y) no-Aux                     | pure          |       6.329 |     31.11% |  253.60 |       19.73 | 16.14 |           30.05% |    106.94 |         49.85 | 65.16% |            56.38% |
| PulpMotion MAR (x,y) Aux                        | pure          |       5.079 |     25.15% |  276.80 |       21.55 | 16.01 |           25.88% |     99.26 |         53.55 | 67.74% |            53.59% |
| PulpMotion MAR (x,y,z) no-Aux                   | pure          |       6.828 |     34.70% |  251.59 |       18.52 | 16.16 |           30.57% |    123.78 |         47.66 | 60.69% |            57.49% |
| PulpMotion MAR (x,y,z) Aux                      | pure          |       5.139 |     27.38% |  258.54 |       20.48 | 17.05 |           26.65% |    113.30 |         51.19 | 63.72% |            55.39% |
| StoryMotion independent-dropout cfg=2.0 eta=1.0 | mixed         |       0.535 |      7.89% |  155.73 |       23.95 | 26.05 |           36.43% |     85.70 |         33.52 | 37.40% |            62.83% |

PulpMotion DiT `(x,y,z) Aux` 的 mixed 与 pure 两行来自 5090 本地 PulpMotion bugfix rerun：联网核对 `robincourant/pulp-motion` official `src/samplers/generation/ddpm.py` 后确认，Standard CFG 分支在 `cfg_rate_z > 0` 且 `joint_in_channels > 0` 时直接把 `grad_z_xy` 加到 `uncond_D_xyz`，没有像 MAR 分支那样补回 z 维，因此 official 原代码会 shape mismatch。5090 本地补丁只把 Standard CFG 的 projection gradient 补回 z 维，原文件备份为 `ddpm.py.bak_20260616_standard_cfg_xyz_aux`。R3 为 official callback 输出；retrieval 口径与 paper-strict full-set R3 可能不完全一致，因此不作为核心优越性结论。

### 4.2 Paper 指标与 5090 Pulp 指标对比

Paper 行来自 PulpMotion PDF Table 4 mixed subset 与 Table 8 pure subset；5090 行来自本次 official full-test rerun。

| model                         | pure or mixed | source                  | FDframing ↓ | Out-rate ↓ | FDTMR ↓ | TMR-Score ↑ |  R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| ----------------------------- | ------------- | ----------------------- | ----------: | ---------: | ------: | ----------: | ----: | ---------------: | --------: | ------------: | -----: | ----------------: |
| PulpMotion DiT (x,y) no-Aux   | mixed         | Paper                   |        4.90 |     25.98% |  372.61 |       23.50 |  3.67 |           10.72% |     87.07 |         30.75 | 34.28% |            51.62% |
| PulpMotion DiT (x,y) no-Aux   | mixed         | 5090 official rerun     |       5.148 |     26.59% |  377.36 |       23.36 | 11.58 |           10.43% |     88.42 |         31.31 | 35.05% |            50.49% |
| PulpMotion DiT (x,y) Aux      | mixed         | Paper                   |        3.37 |     16.76% |  431.54 |       25.05 |  3.89 |            8.91% |     80.08 |         32.81 | 36.06% |            48.68% |
| PulpMotion DiT (x,y) Aux      | mixed         | 5090 official rerun     |       3.777 |     17.35% |  428.53 |       24.97 | 12.42 |            8.55% |     82.19 |         33.28 | 36.67% |            48.09% |
| PulpMotion DiT (x,y,z) no-Aux | mixed         | Paper                   |        4.18 |     23.88% |  390.08 |       23.88 |  3.22 |           11.58% |     97.45 |         23.34 | 27.40% |            50.80% |
| PulpMotion DiT (x,y,z) no-Aux | mixed         | 5090 official rerun     |       7.242 |     35.98% |  440.91 |       24.21 | 18.95 |            7.68% |    106.77 |         25.29 | 28.36% |            48.11% |
| PulpMotion DiT (x,y,z) Aux    | mixed         | Paper                   |        3.76 |     13.90% |  532.42 |       24.58 |  6.13 |            6.88% |    106.97 |         24.61 | 27.43% |            43.36% |
| PulpMotion DiT (x,y,z) Aux    | mixed         | 5090 local bugfix rerun |       5.872 |     24.81% |  519.55 |       25.56 | 19.77 |            6.18% |    114.18 |         26.16 | 28.65% |            42.78% |
| PulpMotion MAR (x,y) no-Aux   | mixed         | Paper                   |        8.51 |     40.75% |  275.30 |       21.68 | 10.60 |           17.10% |    117.77 |         42.84 | 42.69% |            54.89% |
| PulpMotion MAR (x,y) no-Aux   | mixed         | 5090 official rerun     |       8.122 |     42.92% |  277.38 |       20.71 | 16.49 |           19.98% |    125.47 |         38.22 | 39.29% |            54.67% |
| PulpMotion MAR (x,y) Aux      | mixed         | Paper                   |        6.42 |     33.65% |  301.39 |       24.46 | 11.28 |           14.14% |    108.74 |         45.96 | 45.39% |            53.67% |
| PulpMotion MAR (x,y) Aux      | mixed         | 5090 official rerun     |       6.399 |     36.18% |  296.96 |       23.53 | 17.06 |           16.15% |    113.97 |         41.94 | 42.23% |            55.10% |
| PulpMotion MAR (x,y,z) no-Aux | mixed         | Paper                   |        8.66 |     37.50% |  268.41 |       20.13 | 10.59 |           19.83% |    148.12 |         38.58 | 38.34% |            51.74% |
| PulpMotion MAR (x,y,z) no-Aux | mixed         | 5090 official rerun     |       9.608 |     42.34% |  276.66 |       19.07 | 26.18 |           20.47% |    153.61 |         36.86 | 36.57% |            50.65% |
| PulpMotion MAR (x,y,z) Aux    | mixed         | Paper                   |        6.48 |     30.19% |  288.23 |       22.71 | 11.27 |           16.26% |    143.10 |         41.03 | 40.71% |            49.68% |
| PulpMotion MAR (x,y,z) Aux    | mixed         | 5090 official rerun     |       7.392 |     34.21% |  285.07 |       21.82 | 27.32 |           17.51% |    149.33 |         39.67 | 38.96% |            48.72% |
| PulpMotion DiT (x,y) no-Aux   | pure          | Paper                   |        6.78 |     36.25% |  372.75 |       20.74 | 18.16 |           12.73% |     93.37 |         35.99 | 48.82% |            44.56% |
| PulpMotion DiT (x,y) no-Aux   | pure          | 5090 official rerun     |       7.404 |     39.54% |  375.01 |       20.53 | 10.29 |           14.90% |     94.84 |         35.69 | 49.05% |            48.33% |
| PulpMotion DiT (x,y) Aux      | pure          | Paper                   |        5.03 |     24.92% |  424.81 |       21.80 | 18.32 |           11.69% |     91.36 |         38.42 | 51.61% |            40.94% |
| PulpMotion DiT (x,y) Aux      | pure          | 5090 official rerun     |       5.893 |     28.47% |  414.80 |       21.66 | 10.54 |           13.82% |     93.27 |         37.78 | 51.27% |            44.81% |
| PulpMotion DiT (x,y,z) no-Aux | pure          | Paper                   |        5.56 |     29.81% |  334.29 |       18.04 | 15.52 |           17.46% |    108.05 |         28.62 | 41.91% |            45.83% |
| PulpMotion DiT (x,y,z) no-Aux | pure          | 5090 official rerun     |       9.871 |     46.35% |  405.26 |       20.52 |  9.38 |           13.08% |     92.75 |         33.35 | 45.99% |            52.23% |
| PulpMotion DiT (x,y,z) Aux    | pure          | Paper                   |        4.66 |     23.61% |  438.38 |       19.47 |  4.85 |           14.78% |     83.65 |         30.80 | 41.30% |            47.06% |
| PulpMotion DiT (x,y,z) Aux    | pure          | 5090 local bugfix rerun |       7.285 |     35.41% |  435.10 |       21.93 | 17.44 |           12.71% |     86.20 |         35.53 | 49.49% |            49.10% |
| PulpMotion MAR (x,y) no-Aux   | pure          | Paper                   |        6.55 |     30.19% |  251.94 |       20.16 | 25.48 |           28.25% |    108.28 |         52.17 | 67.31% |            55.48% |
| PulpMotion MAR (x,y) no-Aux   | pure          | 5090 official rerun     |       6.329 |     31.11% |  253.60 |       19.73 | 16.14 |           30.05% |    106.94 |         49.85 | 65.16% |            56.38% |
| PulpMotion MAR (x,y) Aux      | pure          | Paper                   |        4.90 |     24.28% |  281.39 |       21.90 | 26.43 |           17.48% |    100.66 |         55.43 | 69.76% |            47.87% |
| PulpMotion MAR (x,y) Aux      | pure          | 5090 official rerun     |       5.079 |     25.15% |  276.80 |       21.55 | 16.01 |           25.88% |     99.26 |         53.55 | 67.74% |            53.59% |
| PulpMotion MAR (x,y,z) no-Aux | pure          | Paper                   |        6.10 |     30.11% |  242.81 |       19.23 | 25.17 |           30.33% |    116.75 |         49.52 | 63.14% |            55.81% |
| PulpMotion MAR (x,y,z) no-Aux | pure          | 5090 official rerun     |       6.828 |     34.70% |  251.59 |       18.52 | 16.16 |           30.57% |    123.78 |         47.66 | 60.69% |            57.49% |
| PulpMotion MAR (x,y,z) Aux    | pure          | Paper                   |        4.30 |     23.48% |  262.34 |       21.08 | 10.30 |           19.26% |    108.98 |         52.36 | 66.16% |            49.72% |
| PulpMotion MAR (x,y,z) Aux    | pure          | 5090 official rerun     |       5.139 |     27.38% |  258.54 |       20.48 | 17.05 |           26.65% |    113.30 |         51.19 | 63.72% |            55.39% |

5090 rerun 与 paper 表不是同一统计对象：paper 报告 Table 4/Table 8 的 subset 结果，5090 本次为 official full-test rerun；因此第二张表用于对照 official pipeline 可复现实测值，不把差异解释为模型优劣变化。

### 4.3 Completion Modes

Completion modes 区分 train/test split。Mixed 行使用 StoryMotion independent-dropout checkpoint 与 mixed full test；pure 行使用 pure-trained checkpoint `gpu1_expA_clean_pure_full_b128_official_92950_20260612_0058` 与 pure full test。Camera completion 给定 human branch，只评估 camera-side metric；human completion 给定 camera branch，只评估 human-side metric。它们是 StoryMotion 的额外能力，不与 PulpMotion text-only joint generation 作同任务横向比较。

| split | mode              | task                  | evaluated samples | FDTMR ↓ | TMR-Score ↑ |  R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| ----- | ----------------- | --------------------- | ----------------: | ------: | ----------: | ----: | ---------------: | --------: | ------------: | -----: | ----------------: |
| mixed | Camera completion | text + human → camera |             10549 |       - |           - |     - |                - |     14.50 |         54.85 | 63.76% |            87.15% |
| mixed | Human completion  | text + camera → human |             10549 |  126.71 |       18.17 | 21.83 |           84.61% |         - |             - |      - |                 - |
| pure  | Camera completion | text + human → camera |              4053 |       - |           - |     - |                - |     32.05 |         55.33 | 72.82% |            82.19% |
| pure  | Human completion  | text + camera → human |              4053 |  110.70 |       16.27 | 20.80 |           90.03% |         - |             - |      - |                 - |

Human completion full sampler/CFG ablation 已补齐到 10549 samples：

| checkpoint          | task             | cfg / eta       | FDTMR ↓ | TMR-Score ↑ |  R3 ↑ | Human Coverage ↑ | 证据                                                                            |
| ------------------- | ---------------- | --------------- | ------: | ----------: | ----: | ---------------: | ----------------------------------------------------------------------------- |
| independent-dropout | human completion | cfg=1.0 eta=0.0 |  126.39 |       18.19 | 21.77 |           84.43% | `v3_closure_20260616/completion_ablation/indepdrop_human_full_cfg1_eta0.json` |
| independent-dropout | human completion | cfg=2.0 eta=1.0 |  126.71 |       18.17 | 21.83 |           84.61% | `p1_parallel_20260615/indepdrop_human_full_cfg2.0_eta1.0.json`                |
| independent-dropout | human completion | cfg=3.0 eta=0.0 |  127.16 |       18.15 | 21.76 |           84.58% | `v3_closure_20260616/completion_ablation/indepdrop_human_full_cfg3_eta0.json` |

### 4.4 Long-Training Replacement Probe

2026-06-17 CST 已完成 GPU1 stable best 与 GPU3 risky best 的 mixed full official probe，均通过 `_best_eval_wrappers/<run>/last.pt -> best_eval.pt` 加载正确 checkpoint。结论是不替代当前正式 independent-dropout checkpoint。

| checkpoint                  |   step | task  | FDframing ↓ | Out-rate ↓ | FDTMR ↓ | TMR-Score ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| --------------------------- | -----: | ----- | ----------: | ---------: | ------: | ----------: | ---------------: | --------: | ------------: | -----: | ----------------: |
| current independent-dropout | 146000 | joint |       0.535 |      7.89% |  155.73 |       23.95 |           36.43% |     85.70 |         33.52 | 37.40% |            62.83% |
| GPU1 stable best            | 282000 | joint |       0.396 |      6.25% |  151.28 |       23.51 |           36.40% |     46.28 |         40.60 | 44.72% |            70.10% |
| GPU3 risky best             | 177500 | joint |       0.540 |      8.22% |  153.03 |       24.32 |           37.41% |     78.75 |         36.68 | 40.21% |            65.10% |

| checkpoint       |   step | completion task | FDTMR ↓ | TMR-Score ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| ---------------- | -----: | --------------- | ------: | ----------: | ---------------: | --------: | ------------: | -----: | ----------------: |
| GPU1 stable best | 282000 | camera          |       - |           - |                - |     14.80 |         55.16 | 63.31% |            85.60% |
| GPU1 stable best | 282000 | human           |  125.45 |       18.26 |           84.83% |         - |             - |      - |                 - |
| GPU3 risky best  | 177500 | camera          |       - |           - |                - |     19.09 |         52.83 | 60.78% |            86.07% |
| GPU3 risky best  | 177500 | human           |  127.25 |       18.13 |           83.89% |         - |             - |      - |                 - |

GPU1 stable best 明显改善 geometry 与 camera semantic 指标，但 joint TMR-Score 从当前 23.95 降到 23.51；GPU3 risky best 的 joint TMR-Score 升到 24.32，但 FDframing=0.540、Out-rate=8.22% 与 raw-skeleton contact gate 不优于当前。两个候选都不满足“official metrics 与 raw-skeleton gate 同时不退化”的 replacement standard。

### 4.5 渲染层面对比

当前可引用的 corrected render evidence 是 `runs/eval/stage2/` 下的 fair-compare 包。`linkedCodebases/StoryMotion/stage2/` 已硬替换为同一正确 evidence tree；替换前的旧 skeleton 图不进入结论。

| render package | checkpoint | configs | samples | 证据文件 |
| --- | --- | ---: | ---: | --- |
| `joint_channel_gated_pulpmotion_fair_compare_20260615` | independent-dropout | 4 | 2 | `manifest.json`、各 config 的 `render_summary.json`、每 sample 的 `summary.json` |
| `gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616` | observed-selfcond best | 4 | 2 | `manifest.json`、各 config 的 `render_summary.json`、每 sample 的 `summary.json` |
| `v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare` | GPU1 stable best | 4 | 2 | `manifest.json`、各 config 的 `render_summary.json`、每 sample 的 `summary.json` |
| `v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare` | GPU3 risky best | 4 | 2 | `manifest.json`、各 config 的 `render_summary.json`、每 sample 的 `summary.json` |
| `native_projection_fair_compare_20260617` | independent-dropout | 4 | 2 | PulpMotion `wz0/wc11` 与 `wz2/wc11` 增加 native camera projection MP4；`manifest.json` 记录 story checkpoint step 146000 |

`std_cfg2.0_eta1.0` 两样本 raw-skeleton gate 汇总如下：

| checkpoint | story human MPJPE ↓ | story human contact diff ↓ | story joint MPJPE ↓ | story joint contact diff ↓ | PulpMotion wz2 MPJPE ↓ | PulpMotion wz2 contact diff ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| independent-dropout | 0.046 | 0.072 | 0.187 | 0.002 | 0.138 | 0.392 |
| GPU1 stable best | 0.048 | 0.024 | 0.167 | 0.061 | 0.138 | 0.392 |
| GPU3 risky best | 0.046 | 0.069 | 0.182 | 0.105 | 0.138 | 0.392 |

渲染层面的结论只限于 sample-level diagnostic：

1. Corrected renderer 使用 decoded raw joints 与 shared render context，可对比 GT、PulpMotion `wz0/wc11`、PulpMotion `wz2/wc11`、StoryMotion human completion 与 StoryMotion joint generation。`joint_fair_concat.mp4` 与 `fair_compare.png` 支持视觉核查，`motion_stats` 支持数值核查。
2. StoryMotion human completion 在给定 camera branch 时 root-aligned MPJPE 明显低于 StoryMotion joint generation；但这不能推出 text-only joint human motion 已解决。
3. GPU1 stable best 改善 `story_joint` MPJPE，但 contact diff 从 current 的 0.002 升到 0.061；GPU3 risky best 的 contact diff 为 0.105。raw-skeleton gate 因此不支持替换当前 checkpoint。
4. Foot/contact proxy 与 MPJPE 存在 tradeoff。这个 gate 支持“不能只看 official aggregate metric 或 MPJPE”，但样本数只有 2，不能声明 human-motion perceptual quality 已优于 PulpMotion。
5. `native_projection_fair_compare_20260617` 补齐了 PulpMotion native camera projection render：每个 sample 有 `pulpmotion_wz0_wc11_native_camera_projection.mp4`、`pulpmotion_wz2_wc11_native_camera_projection.mp4` 与 `pulpmotion_native_camera_projection_concat.mp4`，用于检查 PulpMotion 官方 camera/human 组合在 native camera 视角下的人体投影表现。

### 4.6 Completion TMR-Score 剖析

现象：human completion 的 TMR-Score 明显低于 joint generation。Mixed full test 中，current joint generation TMR-Score 为 23.95，而 current human completion 为 18.17；但 human completion 的 FDTMR=126.71 与 Human Coverage=84.61% 反而优于 joint 的 FDTMR=155.73 与 Human Coverage=36.43%。这说明 completion 低 TMR 不等同于 human branch 完全坏掉，更像是 caption retrieval alignment 下降、分布覆盖变宽，以及 observed camera branch 强约束共同作用。

已有证据支持以下初步判断：

| 假设                                   | 已完成验证                                                                                                                                                                                                                                                | 初步判断                                                                                                  | 后续验证                                                                                           |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 训练分布问题                               | long-training human full eval：GPU1 stable best TMR=18.26、GPU3 risky best TMR=18.13，仍接近 current 18.17；current camera completion 强但 human completion TMR 不随 long training 明显提升                                                                         | 仅延长当前 objective 或重选 latent-loss checkpoint，不能把 human completion TMR 拉近 joint generation               | 需要 task-balanced text-alignment objective 或 branch-specific guidance 训练，而不是只靠 best latent loss |
| Observed branch 压制 text conditioning | mixed condition-reliance 4096-sample 显示 visible delta 远大于 text delta；新增 full-set whole camera-block gate 中，current base human loss median=0.0027，camera shuffle=0.3373、camera zero=0.2268、camera noise=0.8372；GPU1/GPU3 best 也有同量级 whole-block delta | observed camera branch 是 human completion 的主信号，text 是弱信号；这能解释 high coverage 与 low TMR 同时出现            | 需要 sampler-level text-zero/text-shuffle full metric，不能只看 one-step x0-MSE                       |
| 数据/任务定义问题                            | human completion 给定 camera branch 后，camera latent 已编码轨迹、取景和部分动作约束；full-test human completion coverage 高达 84% 以上，但 TMR 停在 18 左右                                                                                                                       | completion target 与 caption 的一一语义对应弱于 text-only joint generation，这是任务定义差异，不应与 PulpMotion joint 行直接排优劣 | 需要 GT observed camera、camera-shuffle、text-shuffle 三组 official metric 对照                        |
| Evaluator 偏置                         | 目前 TMR callback 仍按 full human motion 与 caption 的检索式匹配计分；conditional completion 的目标是 camera/text 条件下补 human target                                                                                                                                    | evaluator-task mismatch 仍是合理解释，但尚未直接证明                                                                | 加 GT observed camera + GT human oracle、text-shuffle TMR、camera-shuffle TMR 对照                  |
| Sampling/CFG 问题                      | full human completion cfg=1/eta=0 TMR=18.19，cfg=2/eta=1 TMR=18.17，cfg=3/eta=0 TMR=18.15；FDTMR 与 coverage 也只小幅波动                                                                                                                                      | standard CFG/eta 不是 5 点以上 TMR gap 的主因                                                                 | 后续若做 guidance，应改成 branch-specific guidance 或训练期 text-alignment，而不是继续扫单一 CFG                    |

新增 full-set intervention probe 已完成四个强对照：

| probe | evaluated samples | FDTMR ↓ | TMR mm-distance ↓ | R3 ↑ | Human Coverage ↑ | 对 baseline 的解释 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| baseline human completion cfg=2 eta=1 | 10549 | 126.71 | 49.48 | 21.83% | 84.61% | `p1_parallel_20260615/indepdrop_human_full_cfg2.0_eta1.0.json` |
| zero camera-text half | 10549 | 126.20 | 49.45 | 21.71% | 84.67% | 与 baseline 几乎同量级，说明 camera text half 不是当前 human completion 的主信号 |
| shuffle camera-text half | 10549 | 126.56 | 49.48 | 21.64% | 84.53% | 与 baseline 几乎同量级，说明 camera text half 的样本级配对也不是当前 human completion 的主信号 |
| zero observed camera latent block | 10549 | 1914.00 | 50.59 | 6.85% | 0.14% | 分布与 retrieval 大幅崩溃，说明 observed camera latent block 对 human completion 是强条件 |
| shuffle observed camera latent block | 10549 | 192.49 | 53.50 | 7.24% | 57.04% | 比 baseline 明显退化但不如 zero 崩溃，说明 observed camera latent block 的真实样本配对携带关键条件信息 |

`shuffle_camera` text 与 `shuffle` camera latent full metric 已于 2026-06-17T16:22+08:00 写出 JSON 并同步本地。`zero_human` / `shuffle_human` / `zero_all` text 与 `noise_matched` camera latent full metric 仍在 5090 跑；截至 2026-06-17T16:30+08:00 尚未写出 JSON，因此不进入完成结论。

初步结论：completion TMR 低主要不是“模型不能生成 human”，而是当前 conditional task 的 observed camera latent branch 对 target human 预测贡献远大于 camera text，TMR 又偏向 text-only full human-caption 检索语义。这个结论有 full-test JSON、completion CFG full ablation、condition-reliance JSON、full-set whole camera-block gate 与新增 text shuffle / camera-latent shuffle full metric 支撑；但 evaluator bias、human-text-half sensitivity、camera-latent noise sensitivity 与 true camera component-level causality 仍需额外实验。

### 4.7 Stage1 Reconstruction Upper Bound

Stage1 upper-bound probe 用 PulpMotion frozen autoencoder 对 GT feature 做 encode/decode，再走同一 official callbacks。它不是生成模型结果，而是“tokenizer reconstruction ceiling”。

| split | evaluated samples | task | FDTMR ↓ | TMR mm-distance ↓ | Human R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | Camera R3 ↑ | Camera Coverage ↑ | FDframing ↓ | Out-rate ↓ |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pure | 4053 | camera | - | - | - | - | 17.66 | 34.62% | 84.68% | - | - |
| pure | 4053 | human | 109.34 | 50.18 | 20.13% | 92.43% | - | - | - | - | - |
| pure | 4053 | joint | 109.34 | 50.18 | 20.13% | 92.43% | 17.66 | 34.62% | 84.68% | 0.137 | 3.47% |

与 StoryMotion Stage2 mixed current 对比只能作为尺度参考，不能直接排纯集/混合集优劣。pure Stage1 reconstruction 的 FDTMR=109.34、Human Coverage=92.43%、FDCLaTr=17.66、Camera Coverage=84.68%、FDframing=0.137，说明 frozen tokenizer 本身的 reconstruction ceiling 明显高于当前 Stage2 generation；Stage2 的主要误差来自 diffusion generation / conditioning，而不是 autoencoder 必然上限。mixed Stage1 full 作业已用 `667551e` 的 PRDC CPU-offload 修复重跑，但截至本文更新时间只写到 640/10549，未产出 full JSON。

---

## 5. 统一结论

1. StoryMotion 的 joint generation、camera completion 与 human completion 均已通过 mixed full-test official evaluator；completion modes 是额外条件生成能力，不与 PulpMotion text-only joint generation 混作同任务比较。
2. PulpMotion paper 中 16 个 core setting 已完成 5090 full-test audit：14 个 setting 可用官方 pipeline 直接复跑；DiT `(x,y,z) Aux` 的 mixed 与 pure 两行依赖本地 Standard CFG 维度对齐 bugfix 后复跑，需与直接 official rerun 分开标注。
3. 在 mixed full joint generation 上，StoryMotion 当前均衡设置显著改善 FDframing、Out-rate、FDTMR、Human Coverage 与 Camera Coverage；但 TMR-Score、FDCLaTr、CLaTr-Score 与 F1 不支配所有 PulpMotion Aux/MAR setting。
4. Completion modes 已补齐 mixed 与 pure full-test 指标：camera completion 的 camera-side semantic 指标强，human completion 的 human-side coverage 高但 TMR-Score 明显低于 joint generation；condition-reliance 与 full-set whole camera-block gate 显示 observed branch 对 completion 的影响远强于 text perturbation。
5. Corrected render evidence 支持把 human completion、joint generation 与 PulpMotion 放在同一 raw-skeleton render context 下比较；但样本数仍小，且 foot/contact proxy 与 MPJPE 存在 tradeoff，因此不能声明 human-motion perceptual quality 已解决。
6. Long-training GPU1/GPU3 candidate 已完成 joint、camera completion、human completion full eval 与 corrected render gate；二者都不满足 replacement gate，当前正式 checkpoint 不替换。
7. 2026-06-17 新增代码已推到 GitHub `main`：`667551e Offload Stage1 PRDC metric states to CPU`。5090 仓库已对齐到 `origin/main`，并在 2026-06-17T15:54+08:00 通过 `ssh -T git@github.com` 认证检查。
8. 截至 2026-06-17T16:30+08:00，5090 仍有 Stage1 mixed full、human text zero-human、human camera-latent noise-matched 等 full metric 作业运行中；它们未产出 JSON，不进入完成结论。
9. 截至 2026-06-17T16:33+08:00，上述运行中作业因 5090 `/dev/sda` 介质错误已全部停止；救援状态与恢复前置条件见 [[2026-06-17_storymotion-5090-sda-failure-rescue]]。

---

## 6. 状态矩阵

| 条目                                                    | 状态        | 可支持结论                                                                                              |
| ----------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------- |
| 单一 Stage2 覆盖三种 generation modes                       | 已验证       | 一个模型支持 joint generation、camera completion 与 human completion                                       |
| Joint generation mixed full-test 对比 PulpMotion matrix | 已验证       | StoryMotion 在 geometry、FDTMR 与 coverage 上优势明确，但不支配所有 semantic 指标                                   |
| PulpMotion 16-setting full-test audit                 | 已验证       | 14 个 setting 可 direct official rerun；DiT `(x,y,z) Aux` 的 2 个 setting 需 local bugfix rerun          |
| Completion modes full-test metrics                    | 已验证       | mixed 与 pure 均已补齐；camera completion 强，human completion 可用但 semantic alignment 仍弱于 joint generation |
| Corrected render evidence                             | 小样本已验证    | 可用于排除旧 skeleton 图误导，并支持 raw-skeleton gate；样本数不足以作正式感知质量结论                                          |
| PulpMotion native camera projection render            | 小样本已验证    | `native_projection_fair_compare_20260617` 补齐 PulpMotion native projection MP4，用于视觉核查官方 camera 下的人体投影          |
| Long-training checkpoint replacement                  | 已验证 / 不替换 | GPU1/GPU3 best 均未同时通过 official metrics 与 raw-skeleton gate                                         |
| Raw-skeleton dynamics/contact gate                    | 小样本已验证    | 通过前不声明 human-motion 感知质量优越；current checkpoint 仍是正式选择                                               |
| Human completion 的 camera whole-block dependency      | 部分已验证      | zero / shuffle observed camera latent full metric 与 latent-block gate 都显示强依赖；noise full metric 仍在跑                  |
| Human completion 的 camera-text dependency            | 部分已验证      | zero / shuffle camera-text half 几乎不改变 full metric；human-text-half 与 zero-all text full metric 仍在跑                                        |
| Human completion 的 camera component-level dependency  | 阻塞        | 当前无已审计 component-to-latent 映射，不声明 component-level camera causality                                 |
| Stage1 autoencoder reconstruction upper bound          | 部分已验证      | pure split full 已完成；mixed split full 因 PRDC GPU state OOM 已修复并重跑中                                          |
| Paper 指标与 5090 Pulp 指标对照                              | 已验证       | paper subset 数值与 5090 full rerun 分开记录，不混作同一统计对象                                                    |

### 6.1 待验证项落地实验

| 待验证项                                                 | 输入 / checkpoint / split                                                                                                                                                                                                                | 命令或脚本                                                                                                                                                                                                                                                                       | 输出路径                                                                                                                                                                                   | 成功标准                                                                                                                                                                                                   | 当前状态                                                                                            |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| Long-training checkpoint replacement                 | GPU1 stable best `p2_long_training_20260615/gpu1_humjoint_heavy_cam1_hum4_joint4_b512/best_eval.pt`；GPU3 risky best `p2_followups_20260616/gpu3_jointheavy6_humanbranch_h2_from146k_to196k/best_eval.pt`；mixed full test 10549 samples | `scripts/storymotion_official_full_eval.py --task joint/camera/human --cfg-scale 2.0 --eta 1.0 --samples 0 --batch-size 64`；5090 使用 `_best_eval_wrappers/<run>/last.pt -> best_eval.pt` symlink wrapper                                                                     | `runs/eval/stage2/v3_closure_20260616/full/gpu1_humjoint_besteval_{joint,camera,human}_std_cfg2_eta1.json` 与 `.../gpu3_jointheavy_h2_besteval_{joint,camera,human}_std_cfg2_eta1.json` | 至少不弱于 current official checkpoint 的 FDframing=0.535、Out-rate=7.89%、FDTMR=155.73、TMR=23.95、FDCLaTr=85.70、CLaTr=33.52、F1=37.40%，且 raw-skeleton gate 不退化                                                  | 已完成；GPU1 geometry/camera stronger but TMR lower，GPU3 TMR higher but geometry/contact weaker；不替换 |
| Raw-skeleton dynamics/contact gate                   | Corrected render source `runs/eval/stage2/joint_channel_gated_cfg_matrix_20260615/`；candidate ckpt 为 GPU1 stable best 与 GPU3 risky best；same two sample IDs                                                                            | `scripts/render_pulpmotion_fair_compare.py --source-render-dir runs/eval/stage2/joint_channel_gated_cfg_matrix_20260615 --story-ckpt <candidate>/best_eval.pt --story-channel-gated-cfg --out-dir runs/eval/stage2/v3_closure_20260616/<candidate>_pulpmotion_fair_compare` | `runs/eval/stage2/v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare/` 与 `.../gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare/`                                    | `manifest.json` 存在；每 config 有 `joint_fair_concat.mp4`、`fair_compare.png`、`render_summary.json`；`story_joint` 的 foot-contact absdiff 与 MPJPE 不劣于 current independent-dropout corrected render，并无空白/错误骨架 | 已完成小样本 gate；GPU1/GPU3 contact gate 不支持替换，仍不作感知质量优越性声明                                           |
| Human completion sampler / CFG effect                | independent-dropout checkpoint `independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`；mixed full test 10549 samples；task=human                                                                                            | `scripts/storymotion_official_full_eval.py --task human --cfg-scale 1.0 --eta 0.0 --samples 0` 与 `--cfg-scale 3.0 --eta 0.0 --samples 0`                                                                                                                                    | `runs/eval/stage2/v3_closure_20260616/completion_ablation/indepdrop_human_full_cfg1_eta0.json` 与 `.../indepdrop_human_full_cfg3_eta0.json`                                             | 若 cfg=1/3 仍在 18 左右，则 standard CFG/eta 不是低 TMR 主因；若显著升近 joint TMR，则重选 completion sampler                                                                                                                | 已完成；TMR=18.19/18.15，与 cfg=2 的 18.17 基本一致                                                        |
| Human completion 的 camera whole-block dependency     | independent-dropout current、GPU1 stable best、GPU3 risky best；mixed full test cache 10549 samples                                                                                                                                       | `scripts/storymotion_stage2_gated_eval.py modeb-gate --samples 0 --split val`，对 observed camera latent block 做 shuffle/zero/noise matched 扰动                                                                                                                                | `runs/eval/stage2/v3_closure_20260616/latent_block_gate/indepdrop_current_modeb_gate.json`、`gpu1_humjoint_besteval_modeb_gate.json`、`gpu3_jointheavy_h2_besteval_modeb_gate.json`      | camera block perturbation 后 human completion x0 loss 显著高于 base，且记录 scope 明确为 whole camera latent block                                                                                                 | 已完成；current base median=0.0027，shuffle=0.3373，zero=0.2268，noise=0.8372；GPU1/GPU3 同量级            |
| Human completion full-set text / camera-latent intervention | independent-dropout checkpoint；mixed full test 10549 samples；task=human；cfg=2.0 eta=1.0 | `scripts/storymotion_official_full_eval.py --task human --text-intervention <iv> --camera-latent-intervention <iv>` | `runs/eval/stage2/human_completion_dependency_20260617/` | 若 camera text perturbation 小而 camera latent perturbation 大，则支持 observed camera latent 主导；若 text shuffle 大幅下降，则说明 text semantic alignment 仍显著 | 部分完成：`zero_camera` 与 `shuffle_camera` text 几乎不变；`zero` camera latent 崩溃；`shuffle` camera latent 明显退化；`noise_matched` 与 human-text-half 仍在 5090 跑 |
| Stage1 autoencoder reconstruction upper bound | PulpMotion frozen Stage1 autoencoder；pure/mixed test split；official metric callbacks | `scripts/eval_stage1_pulp_autoencoder_official.py --set-name pure_/mixed_ --samples 0` | `runs/eval/stage1/official_upper_bound_20260617/` | Stage1 reconstruction full metric 给出 tokenizer ceiling；mixed full 不能因 PRDC GPU memory OOM 中断 | pure full 已完成；mixed full 已用 `667551e` PRDC CPU-offload 修复重跑，当前仍在 5090 跑 |
| PulpMotion native camera projection render | independent-dropout checkpoint；source render dir `runs/eval/stage2/bilateral_cfg_renders_20260614`；same two sample IDs | `scripts/render_pulpmotion_fair_compare.py --out-dir runs/eval/stage2/native_projection_fair_compare_20260617 --pulp-cfg-z 0.0 2.0` | `runs/eval/stage2/native_projection_fair_compare_20260617/` | `manifest.json` 存在；4 configs × 2 samples 均有 native projection MP4；PulpMotion single-projection concat bug 不复发 | 已完成；StoryMotion code 提交 `667551e` 已推送 |
| Human completion 的 camera component-level dependency | independent-dropout checkpoint；需要 camera latent / raw camera component 的可信映射                                                                                                                                                           | 先审计 PulpMotion camera feature layout、autoencoder encode/decode contract 与 latent subchannel 可解释性；若无法建立映射，不运行 component perturbation                                                                                                                                         | 计划输出 `runs/eval/stage2/v3_closure_20260616/camera_component_dependency/`                                                                                                               | 分别扰动 camera translation、rotation/FOV 或经审计的 camera latent component 后，human completion TMR/FDTMR 与 x0-MSE 的 delta 有可解释排序；否则不声明 component causality                                                      | 仍阻塞：现有 cache 只暴露 64-D camera latent block，未发现已审计 component-to-latent 映射；不能伪造按通道分组实验             |

---

## 7. 证据路径

本地 `linkedCodebases/StoryMotion/stage2/` 已于 2026-06-17 直接删除旧树，并用 `linkedCodebases/StoryMotion/runs/eval/stage2/` 镜像重建；正式证据仍以 `runs/eval/stage2/` 路径为准。

Full-test 主要指标：

- `linkedCodebases/StoryMotion/runs/eval/stage1/official_upper_bound_20260617/stage1_pure_full.json`
- `linkedCodebases/StoryMotion/runs/eval/stage1/official_upper_bound_20260617/stage1_mixed_full_offload_retry.log`（running，尚无 full JSON）
- `linkedCodebases/StoryMotion/runs/eval/stage2/pulpmotion_official_matrix_20260616/full/`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p1_parallel_20260615/indepdrop_joint_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p1_parallel_20260615/indepdrop_camera_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p1_parallel_20260615/indepdrop_human_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p1_parallel_20260615/puretrain_camera_pure_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p1_parallel_20260615/puretrain_human_pure_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v3_closure_20260616/completion_ablation/`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v3_closure_20260616/latent_block_gate/`
- `linkedCodebases/StoryMotion/runs/eval/stage2/human_completion_dependency_20260617/human_text_zero_camera_full.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/human_completion_dependency_20260617/human_camera_latent_zero_full.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/human_completion_dependency_20260617/human_text_shuffle_camera_full.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/human_completion_dependency_20260617/human_camera_latent_shuffle_full.json`

渲染与 raw-skeleton gate：

- `linkedCodebases/StoryMotion/runs/eval/stage2/joint_channel_gated_pulpmotion_fair_compare_20260615/manifest.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616/manifest.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare/manifest.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare/manifest.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/native_projection_fair_compare_20260617/manifest.json`

诊断与训练支持：

- `linkedCodebases/StoryMotion/runs/eval/stage2/stage2_mixed_condition_reliance_20260612/mixed_standard_ema_sched_last.pt_condition_reliance.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/stage2_mixed_condition_reliance_20260612/mixed_noema_sched_last.pt_condition_reliance.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/stage2_pure_official_step_condition_reliance_20260612_0051/summary.json`
- `linkedCodebases/StoryMotion/runs/eval/stage2/p2_all_gpu_training_summary_20260616.json`
- `obsidian-vault/paperPDFs/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.pdf`
- [robincourant/pulp-motion `src/samplers/generation/ddpm.py`](https://github.com/robincourant/pulp-motion/blob/main/src/samplers/generation/ddpm.py)
- StoryMotion GitHub `main`: `667551e Offload Stage1 PRDC metric states to CPU`
- `5090:/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/`
- `5090:/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/_best_eval_wrappers/`
