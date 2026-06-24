---
hypothesis: "StoryMotion V4 将 V3 的 full-test 证据推进到 ICLR 级别的可靠性与贡献闭环：三模式统一框架和 joint mode 多指标超过 PulpMotion 是两个候选贡献点，但仍不足以单独支撑强会投稿；第三个贡献点应收敛为 completion 任务的公平内部 baseline、条件依赖诊断与 human-in-camera-projection 可靠性协议。"
status: in_progress
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories|Motion Prompting]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence|PoseAnything]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
  - "[[analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance|DanceCamera3D]]"
  - "[[analysis/CVPR_2024/MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Latent_Diffusion_Model|MCM-LDM]]"
  - "[[analysis/NEURIPS_2023/FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing|FineMoGen]]"
  - "[[analysis/arxiv_2023/VideoComposer_Compositional_Video_Synthesis_with_Motion_Controllability|VideoComposer]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-06-21T13:45:00+08:00
supersedes: "[[2026-06-16_storymotion-v3-formal]]"
---

# StoryMotion V4：ICLR 可靠性与 Completion 贡献闭环

> [!abstract] 核心结论
> StoryMotion V3 已经证明：一个冻结 PulpMotion Stage1 continuous latent tokenizer 加一个 branch-mask Stage2 diffusion，可以统一支持 camera completion、human completion 与 joint generation；在 mixed full-test joint generation 上，StoryMotion 在 FDframing、Out-rate、FDTMR、Human Coverage 与 Camera Coverage 上显著优于 PulpMotion matrix。
>
> 但 V4 判断更严格：当前两个候选贡献点还不够稳。第一，三模式统一框架需要证明不是简单工程拼接，至少要和 fair internal separate-task baselines 对比参数量、训练成本与性能。第二，joint mode 虽在多个指标超越 PulpMotion，但 TMR-Score、FDCLaTr、CLaTr-Score 与 F1 不支配所有 PulpMotion Aux/MAR setting；human motion 的相机投影视觉可靠性也未系统验证。第三，completion mode 是最可能形成 ICLR 第三贡献点的方向，但必须补齐 baseline、任务适配、公平指标与可视化应用。
>
> V4 的优先级不是继续堆指标，而是完成三个闭环：1. human-in-camera-projection render gate；2. completion fair internal baseline；3. joint human quality degradation 的条件依赖诊断与缓解。所有新增渲染输出统一写入 `linkedCodebases/StoryMotion/stage2/vis/`，所有新增指标统一写入 `linkedCodebases/StoryMotion/stage2/metrics/`。

---

## 1. V3 核心证据快照

### 1.1 方法快照

StoryMotion 复用 PulpMotion Stage1 作为冻结 continuous tokenizer：

```text
z = concat([z_hum, z_cam]) in R^{192 x T}
z_hum in R^{128 x T}
z_cam in R^{64 x T}
```

Stage2 是作用于 continuous latent sequence 的 branch-mask diffusion。三种任务只改变 observed branch 与 target branch：

| 模式                | 输入条件                 | 生成分支                  | 评估定位                                     |
| ----------------- | -------------------- | --------------------- | ---------------------------------------- |
| Camera completion | text + human latent  | camera latent         | StoryMotion 额外条件生成能力                     |
| Human completion  | text + camera latent | human latent          | StoryMotion 额外条件生成能力                     |
| Joint generation  | text only            | human + camera latent | 与 PulpMotion text-to-joint baseline 公平对比 |

当前 V3 正式设置为 independent-modality-dropout fine-tuning + 50-step DDIM START_X sampler，`cfg=2.0`，`eta=1.0`。

### 1.2 Joint Full-Test 核心结果

V3 已完成 PulpMotion 16-setting full-test audit。14 个 setting 可用官方 checkpoint/config/sampler/evaluator 直接复跑；DiT `(x,y,z) Aux` 的 mixed 与 pure 两行依赖本地 Standard CFG 维度对齐 bugfix 后复跑，需单独标注。

StoryMotion 当前正式 joint mixed full-test 与主要 PulpMotion mixed 行对比如下：

| model                           | split | FDframing ↓ | Out-rate ↓ | FDTMR ↓ | TMR-Score ↑ |  R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| ------------------------------- | ----- | ----------: | ---------: | ------: | ----------: | ----: | ---------------: | --------: | ------------: | -----: | ----------------: |
| PulpMotion DiT `(x,y)` no-Aux   | mixed |       5.148 |     26.59% |  377.36 |       23.36 | 11.58 |           10.43% |     88.42 |         31.31 | 35.05% |            50.49% |
| PulpMotion DiT `(x,y)` Aux      | mixed |       3.777 |     17.35% |  428.53 |       24.97 | 12.42 |            8.55% |     82.19 |         33.28 | 36.67% |            48.09% |
| PulpMotion MAR `(x,y)` Aux      | mixed |       6.399 |     36.18% |  296.96 |       23.53 | 17.06 |           16.15% |    113.97 |         41.94 | 42.23% |            55.10% |
| PulpMotion MAR `(x,y,z)` Aux    | mixed |       7.392 |     34.21% |  285.07 |       21.82 | 27.32 |           17.51% |    149.33 |         39.67 | 38.96% |            48.72% |
| StoryMotion independent-dropout | mixed |       0.535 |      7.89% |  155.73 |       23.95 | 26.05 |           36.43% |     85.70 |         33.52 | 37.40% |            62.83% |

可支持的正式说法：

1. StoryMotion 在 camera-human geometry、FDTMR、Human Coverage 与 Camera Coverage 上有强优势。
2. StoryMotion 不支配所有 semantic 指标：TMR-Score 低于 PulpMotion DiT Aux，CLaTr-Score 与 F1 低于 PulpMotion MAR Aux。
3. 因此 joint result 是一个 solid but not dominant 的贡献点，不能单独支撑“全面 SOTA”叙事。

### 1.2.1 逐指标解释

下表先独立解释每个指标，避免把多指标合并成一个笼统的“质量”判断。

| 指标 | 越高/越低越好 | 独立含义 | 解释注意事项 |
| --- | --- | --- | --- |
| FDframing | 越低越好 | generated human-camera 投影关系与参考分布之间的 Fréchet distance，主要衡量 framing geometry 的分布接近程度 | 低 FDframing 只说明相机与人体几何关系更接近数据分布，不能单独证明 human motion 自然 |
| Out-rate | 越低越好 | 人体投影落出有效画面或 framing 约束失败的比例 | 是 camera-human composition 失败率，不等价于 semantic alignment |
| FDTMR | 越低越好 | TMR feature 空间中 generated human motion distribution 与 reference human distribution 的 Fréchet distance | 更偏 distribution-level human motion 质量，不直接衡量单个 caption 是否被正确执行 |
| TMR-Score | 越高越好 | TMR encoder 下 human motion 与文本 caption 的检索/匹配分数 | 更贴近 text-only human-caption alignment；conditional completion 中低分可能混合 evaluator-task mismatch 与真实语义退化 |
| R1 / R2 / R3 | 越高越好 | human 或 camera caption retrieval 的 top-k 命中率 | 依赖 official callback 的 retrieval protocol；不同表中的 R3 口径必须跟输出字段对应 |
| Human Coverage | 越高越好 | generated human motion 在 TMR manifold 中覆盖 reference distribution 的比例 | 高 coverage 表示多样性/覆盖范围强，但可能伴随 precision 或 text alignment 下降 |
| FDCLaTr | 越低越好 | CLaTr feature 空间中 generated camera trajectory distribution 与 reference camera distribution 的 Fréchet distance | 主要衡量 camera-side distribution，不说明 human skeleton 动作质量 |
| CLaTr-Score | 越高越好 | CLaTr encoder 下 camera trajectory 与 camera caption 的匹配分数 | 是 camera-caption semantic 指标，不能替代 projection render 或 Out-rate |
| F1 | 越高越好 | camera segment / camera-event 类指标的综合 F1 | 对 camera motion event 或 caption segment 更敏感，不能单独解释整体 cinematic quality |
| Camera Coverage | 越高越好 | generated camera trajectory 在 CLaTr manifold 中覆盖 reference distribution 的比例 | 高 coverage 表示 camera 分布覆盖强，但需要结合 FDCLaTr、CLaTr-Score 与 render 检查可用性 |
| PRDC precision / recall / density / coverage | 通常越高越好 | 在 TMR/CLaTr feature manifold 上衡量 generated distribution 与 reference distribution 的局部邻域关系 | 作为 distribution diagnostic 使用，不能替代 sample-level 视觉验证 |
| Raw-skeleton MPJPE | 越低越好 | decoded raw skeleton 与 GT skeleton 的 root-aligned joint error | 当前只用于小样本 render gate，不作为 full-set official superiority claim |
| Contact proxy diff | 越低越好 | 生成动作与参考动作的 foot/contact proxy 差异 | 是 contact/dynamics diagnostic，可能与 MPJPE 存在 tradeoff，必须和视频一起解释 |

### 1.2.2 指标来源与口径

| 指标组 | 来源组件 | 计算对象 | 本文解释边界 |
| --- | --- | --- | --- |
| FDframing / Out-rate | PulpMotion joint projection callback | decoded human joints + camera + intrinsics 的投影关系 | 只说明 camera-human geometry，不等价于 human perceptual quality |
| FDTMR / TMR-Score / R1-R3 / Human Coverage | PulpMotion HumanMetricCallback / TMR encoder | decoded human motion 与 caption embedding / reference motion distribution | TMR retrieval 更贴近 text-only full motion-caption 对齐；conditional completion 下需谨慎解释 |
| FDCLaTr / CLaTr-Score / R1-R3 / Camera Coverage / F1 | PulpMotion CameraMetricCallback / CLaTr encoder + segment metrics | decoded camera trajectory 与 camera caption / reference distribution | camera-side semantic aggregate，不单独证明 human motion 质量 |
| PRDC coverage / precision / recall / density | PulpMotion ManifoldMetrics | TMR/CLaTr feature manifold | 作为分布覆盖/密度证据，不能替代 sample-level render gate |
| Raw-skeleton MPJPE/contact proxy | StoryMotion corrected fair-compare render summary | decoded raw skeleton sample diagnostics | 仅是小样本 gate，不能作总体优越性结论 |

### 1.3 Completion Full-Test 核心结果

Completion modes 区分 train/test split。Mixed 行使用 independent-dropout checkpoint 与 mixed full test；pure 行使用 pure-trained checkpoint 与 pure full test。

| split | mode | task | samples | FDTMR ↓ | TMR-Score ↑ | R3 ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ | F1 ↑ | Camera Coverage ↑ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed | Camera completion | text + human -> camera | 10549 | - | - | - | - | 14.50 | 54.85 | 63.76% | 87.15% |
| mixed | Human completion | text + camera -> human | 10549 | 126.71 | 18.17 | 21.83 | 84.61% | - | - | - | - |
| pure | Camera completion | text + human -> camera | 4053 | - | - | - | - | 32.05 | 55.33 | 72.82% | 82.19% |
| pure | Human completion | text + camera -> human | 4053 | 110.70 | 16.27 | 20.80 | 90.03% | - | - | - | - |

Completion 的当前解释边界：

1. Camera completion 很强，是最适合作为应用贡献的模式。
2. Human completion 的 FDTMR 与 coverage 强，但 TMR-Score 低，说明它更像 conditional reconstruction / diverse completion，而不是 text-only semantic retrieval 最优。
3. Completion modes 不能直接拿 PulpMotion text-only joint generation 作同任务优劣排序。

### 1.4 Human Completion Dependency 已有证据

已有 full-set intervention probe 显示 human completion 对 observed camera latent 强依赖，对 camera-text half 不敏感：

| probe                                 | samples | FDTMR ↓ | TMR mm-distance ↓ |   R3 ↑ | Human Coverage ↑ | 解释                               |
| ------------------------------------- | ------: | ------: | ----------------: | -----: | ---------------: | -------------------------------- |
| baseline human completion cfg=2 eta=1 |   10549 |  126.71 |             49.48 | 21.83% |           84.61% | 当前正式 human completion            |
| zero camera-text half                 |   10549 |  126.20 |             49.45 | 21.71% |           84.67% | 几乎不变，camera text half 不是主信号      |
| shuffle camera-text half              |   10549 |  126.56 |             49.48 | 21.64% |           84.53% | 几乎不变，camera text 配对不是主信号         |
| zero observed camera latent block     |   10549 | 1914.00 |             50.59 |  6.85% |            0.14% | 分布崩溃，observed camera latent 是强条件 |
| shuffle observed camera latent block  |   10549 |  192.49 |             53.50 |  7.24% |           57.04% | 明显退化，真实 camera 配对携带关键条件          |

V4 需要把这个从“解释现象”推进到“贡献组件”：提出可复现的 conditional-dependency diagnostic protocol，并用它指导 joint human quality repair。

当前证据的解释边界必须收紧：

1. `zero camera-text half` 与 `shuffle camera-text half` 几乎不变，只能说明 **human completion 中 camera-text half 不是主导信号**。
2. 这不能推出“text 被直接忽略”，因为还缺 human-text half、all-text、camera completion 对称实验、sample-level latent/x0 delta 和 projection render。
3. `zero/shuffle observed camera latent block` 的大幅退化说明 observed camera latent 是强条件，但仍不能证明它是唯一条件；它可能与 text、trajectory prior 和 dataset bias 共同作用。
4. 结论措辞应为：observed latent 在当前 human completion 设置下可能获得了高于 camera-text 的处理优先级，而不是“文本完全无效”。

2026-06-18 在 4090 上补了 intervention 代码路径 smoke：

```text
path: runs/eval/stage2/v4_dependency_smoke_20260618_s128/
ckpt: runs/train/stage2/condmdi_pulp_no_proj_20260611/gpu1_main/last.pt
cache: runs/train/stage2/condmdi_pulp_no_proj_20260611/cache_mixed_full_20260614/val.pt
samples: 128
steps: 5
cfg/eta: 2.0 / 0.0
```

已跑通：

| task | intervention | output |
| --- | --- | --- |
| human completion | none | `human_baseline_s128.json` |
| human completion | zero human-text half | `human_zero_human_text_s128.json` |
| human completion | noise-matched observed camera latent | `human_camera_latent_noise_s128.json` |
| camera completion | none | `camera_baseline_s128.json` |
| camera completion | zero camera-text half | `camera_zero_camera_text_s128.json` |
| camera completion | noise-matched observed human latent | `camera_human_latent_noise_s128.json` |

这些 s128 结果同样只用于 smoke：早期 checkpoint 的 absolute metrics 很差，不能与 V3 formal checkpoint 混合解释。它们证明新增 CLI 与 official metric pipeline 可运行，并提供正式 full-set dependency matrix 的模板。正式矩阵应在 independent-dropout checkpoint 上补齐：

| mode | text intervention | observed latent intervention | 必须输出 |
| --- | --- | --- | --- |
| human completion | none / zero_camera / shuffle_camera / zero_human / shuffle_human / zero_all / shuffle_all | none | official human metrics + records |
| human completion | none | zero / shuffle / noise_matched observed camera latent | official human metrics + records |
| camera completion | none / zero_human / shuffle_human / zero_camera / shuffle_camera / zero_all / shuffle_all | none | official camera metrics + records |
| camera completion | none | zero / shuffle / noise_matched observed human latent | official camera metrics + records |
| joint generation | none / zero_human / zero_camera / zero_all / shuffle_all | none | official joint metrics + branch-specific render |
| diagnostic subset | paired baseline vs same-seed intervention | same as above | per-sample latent delta、decoded x0 delta、camera projection videos |

正式判断规则：

1. 若 human-text half 和 all-text 扰动也几乎不变，同时 sample-level decoded x0 delta 很小，才能说 text conditioning 在该 setting 下整体很弱。
2. 若 camera completion 对 zero/shuffle camera-text 敏感，而 human completion 对 human-text 不敏感，则说明 human 分支文本利用存在非对称问题。
3. 若 observed latent noise/shuffle 在两个 completion 方向均造成大幅退化，说明 latent coupling 是双向强条件；若只有 human 方向敏感，则问题更集中于 camera-to-human dominance。
4. 所有结论必须同时参考 official metrics、records、projection render 和失败样本，不能只看 aggregate。

### 1.5 Stage1 Upper Bound 与 Long-Training Probe

Stage1 reconstruction upper bound 已完成 pure full：

| split | task                 | FDTMR ↓ | Human Coverage ↑ | FDCLaTr ↓ | Camera Coverage ↑ | FDframing ↓ | Out-rate ↓ |
| ----- | -------------------- | ------: | ---------------: | --------: | ----------------: | ----------: | ---------: |
| pure  | joint reconstruction |  109.34 |           92.43% |     17.66 |            84.68% |       0.137 |      3.47% |

含义：frozen tokenizer 的 reconstruction ceiling 明显高于当前 Stage2 generation，主要误差来自 diffusion generation / conditioning，而不是 Stage1 必然上限。

Long-training GPU1/GPU3 best 已完成 joint、camera completion、human completion full eval 与 corrected render gate，但不替代当前 checkpoint：

| checkpoint                  | task  | FDframing ↓ | Out-rate ↓ | FDTMR ↓ | TMR-Score ↑ | Human Coverage ↑ | FDCLaTr ↓ | CLaTr-Score ↑ |   F1 ↑ | Camera Coverage ↑ |
| --------------------------- | ----- | ----------: | ---------: | ------: | ----------: | ---------------: | --------: | ------------: | -----: | ----------------: |
| current independent-dropout | joint |       0.535 |      7.89% |  155.73 |       23.95 |           36.43% |     85.70 |         33.52 | 37.40% |            62.83% |
| GPU1 stable best            | joint |       0.396 |      6.25% |  151.28 |       23.51 |           36.40% |     46.28 |         40.60 | 44.72% |            70.10% |
| GPU3 risky best             | joint |       0.540 |      8.22% |  153.03 |       24.32 |           37.41% |     78.75 |         36.68 | 40.21% |            65.10% |

GPU1 改善 geometry/camera semantic 但 TMR 下降；GPU3 TMR 提升但 geometry/contact gate 弱。因此 V4 不应把“长训练自然解决问题”作为路线。

---

## 2. ICLR 贡献判断

### 2.1 当前两个贡献点的强度

候选贡献点 1：三模式统一生成框架。

判断：方向是 solid，但目前还不够完整。审稿人会问：一个 branch-mask model 同时覆盖三种任务，是否只是把三种 mask 拼进同一个 diffusion 训练？如果没有 separate-task baseline 或 branch-mask 消融，就很难证明统一框架本身有研究贡献。

需要补强：

1. 与 three separate models 对比：同 backbone、同 tokenizer、同 split、同训练预算，分别训练 joint/camera/human 三个任务。
2. 报告参数量、训练成本、采样成本、三任务平均性能。
3. 证明 unified branch-mask 至少不显著牺牲主指标，同时用更少参数覆盖三任务。

候选贡献点 2：joint mode 多指标超过 PulpMotion。

判断：这是有效但不完整的实证贡献。FDframing、Out-rate、FDTMR、Human Coverage、Camera Coverage 的优势很强，但语义指标不全面支配，且 human render reliability 未闭环。写法应是“significant gains in geometry, distribution coverage, and selected semantic distribution metrics”，不能写成“全面优于 PulpMotion”。

需要补强：

1. human-in-camera-projection render gate。
2. raw skeleton dynamics/contact 的 sample 数从 2 扩展到至少 50 或 100。
3. per-sample failure taxonomy，避免 aggregate 指标掩盖 human motion 退化。

### 2.2 第三贡献点的建议定义

最稳的第三贡献点不是“completion 也能做”，而是：

> 系统性提出并验证 human-camera conditional completion 任务：在缺失相机或缺失人体的场景中，StoryMotion 使用同一个 branch-mask model 完成 conditional generation；同时构建 fair internal baselines、条件依赖诊断和相机投影可靠性协议，证明 camera completion 的实用优势，并解释 human completion 的 text-alignment 局限。

这个措辞有三个优点：

1. 不声称已有外部 baseline 无法支撑的 SOTA。
2. 把 completion 的应用价值、baseline、公平性和可靠性绑在一起，形成完整贡献。
3. 即使 human completion 的 TMR 不高，也可被解释为 conditional task 与 text-only TMR evaluator 的 mismatch，而不是失败。

### 2.3 不建议的叙事

避免以下说法：

1. “StoryMotion 全面超过 PulpMotion”：不成立，因为 semantic 指标不全面支配。
2. “Human completion 已解决 human generation”：不成立，因为 TMR-Score 低，且视觉可靠性未系统验证。
3. “Joint mode 下 human 与 camera 独立解耦”：当前证据相反，observed camera latent 对 human completion 是强条件，joint mode 可能存在过耦合或 text 弱化。
4. “Completion 直接优于 PulpMotion”：PulpMotion 是 text-only joint generation，不是 same-task completion baseline。

---

## 3. 可靠性验证缺口

### 3.1 当前缺口

用户指出的高优先级缺口成立：已有 skeleton render 和少量 native camera projection render，但还没有系统给出 human motion 在相机投影下的结果。对于 human-camera generation，固定视角 skeleton 只能检查人体动作本身，不能验证以下关键问题：

1. 人是否稳定落在相机画面内。
2. 人体关节点投影是否出现严重抖动、离屏、尺度突变、反向穿越。
3. StoryMotion 的低 FDframing 是否对应视觉可接受的 frame composition。
4. Joint mode 下 human 质量下降是否在 camera projection 中被放大。

因此 V4 需要把渲染 gate 从“固定视角 skeleton diagnostic”升级为“fixed-view skeleton + camera-projection render + per-frame projection metrics”。

### 3.2 目录规范

所有 V4 新增结果统一写入 `linkedCodebases/StoryMotion/stage2/` 下两个一级目录：

```text
linkedCodebases/StoryMotion/stage2/
  vis/
    joint/
      storymotion/
      pulpmotion/
      fair_intra_bl/
    camera_completion/
      storymotion/
      fair_intra_bl/
      oracle_gt_human/
    human_completion/
      storymotion/
      fair_intra_bl/
      oracle_gt_camera/
  metrics/
    joint/
      storymotion/
      pulpmotion/
      fair_intra_bl/
    camera_completion/
      storymotion/
      fair_intra_bl/
      oracle_gt_human/
    human_completion/
      storymotion/
      fair_intra_bl/
      oracle_gt_camera/
```

命名建议：

```text
vis/{mode}/{method}/{run_id}/{sample_id}/
  fixed_skeleton.mp4
  camera_projection.mp4
  fixed_and_projection_concat.mp4
  overlay_gt_vs_pred_projection.mp4
  frames/
  render_meta.json

metrics/{mode}/{method}/{run_id}/
  aggregate_metrics.json
  per_sample_metrics.csv
  per_frame_projection_metrics.csv
  failure_cases.json
  run_meta.json
```

`vis` 只放可视化、帧图和 render metadata；`metrics` 只放 JSON/CSV/log summaries。旧的 `stage2/*fair_compare*` 包可以保留为历史证据，但 V4 新实验不再散落在 stage2 根目录。

### 3.3 Camera Projection Render 必须包含的内容

每个样本至少输出：

1. GT human + GT camera projection。
2. StoryMotion joint human + StoryMotion joint camera projection。
3. StoryMotion human completion human + observed GT camera projection。
4. StoryMotion camera completion camera + observed GT human projection。
5. PulpMotion joint human + PulpMotion camera projection。
6. FairIntra-BL 对应模式 projection。

每个视频必须记录：

1. sample id、caption、split、mode、method、checkpoint、seed、cfg、eta。
2. camera source：GT / generated / PulpMotion / observed。
3. human source：GT / generated / PulpMotion / observed。
4. projection convention：intrinsics、extrinsics、coordinate frame、normalization。
5. frame count、fps、resolution、valid mask。

### 3.4 Projection Metrics

建议最小指标：

| 指标 | 计算对象 | 用途 |
| --- | --- | --- |
| in-frame joint ratio ↑ | projected 2D joints | 衡量人体是否留在画面内 |
| bbox center error ↓ | pred vs GT 2D bbox center | 衡量 framing stability |
| bbox scale error ↓ | pred vs GT 2D bbox size | 衡量 zoom/距离合理性 |
| temporal jitter ↓ | 2D joint / bbox velocity jerk | 衡量画面抖动 |
| projection outlier rate ↓ | NaN、behind-camera、extreme coordinate | 捕捉几何错误 |
| skeleton MPJPE ↓ | raw 3D skeleton | 与固定视角 motion quality 对齐 |
| contact proxy diff ↓ | foot/contact proxy | 防止只优化投影导致人体动力学退化 |

这些指标不替代 official FDframing/TMR/CLaTr，而是作为可靠性 gate。

### 3.5 2026-06-18 4090 实现 Smoke

已补齐并在 4090 上执行 human-in-camera-projection render 的代码路径：

1. `scripts/render_bilateral_results.py` 新增 `--metrics-out-dir`，可将 source render 的 MP4/PNG 写入 `vis`，将 `render_summary.json` 写入 `metrics`。
2. `scripts/render_pulpmotion_fair_compare.py` 新增 camera projection render：`gt_camera_projection.mp4`、`pulpmotion_*_camera_projection.mp4`、`story_camera_camera_projection.mp4`、`story_human_camera_projection.mp4`、`story_joint_camera_projection.mp4` 与 `camera_projection_fair_concat.mp4`。
3. fair-compare summary 新增 `camera_projection_videos`、per-sample `projection_stats` 与 `projection_stats_aggregate`。
4. fair-compare 也新增 `--metrics-out-dir`，正式运行时可以把视频/PNG 放在 `stage2/vis/...`，把 JSON summary/manifest 放在 `stage2/metrics/...`。

4090 smoke 使用的是早期 checkpoint，而不是 V3 independent-dropout formal checkpoint：

```text
ckpt: runs/train/stage2/condmdi_pulp_no_proj_20260611/gpu1_main/last.pt
cache: runs/train/stage2/condmdi_pulp_no_proj_20260611/cache_mixed_full_20260614/val.pt
samples: 1
steps: 5
fps: 6
sample: 2011_-4GsCEopbd4_00008_001_a
```

因此该 smoke 只验证实现、目录规范与 projection stats 管线，不作为 V3/V4 正式性能证据。正式 V3 projection gate 仍需要把 independent-dropout checkpoint/cache/source render 转移到 4090 或恢复 5090 环境后重跑。

输出路径：

```text
stage2/vis/v4_projection_split_smoke_20260618/source/
stage2/metrics/v4_projection_split_smoke_20260618/source/
stage2/vis/v4_projection_split_smoke_20260618/fair_compare/
stage2/metrics/v4_projection_split_smoke_20260618/fair_compare/
```

smoke 中已确认 `vis` 目录含所有 MP4/PNG，`metrics` 目录含 `manifest.json`、`render_summary.json` 与 per-sample `summary.json`。单样本 projection stats 示例显示，`story_human` 与 `story_joint` 均能产出相机投影指标；但因为 checkpoint、步数和样本数都不是正式设置，不解释为方法优劣。

---

## 4. Completion Baseline 与适配设计

### 4.1 现实 baseline 选择

当前没有可直接公开复用的 camera completion 或 human completion baseline。强行改造 MDM、MotionDiffuse、camera-only trajectory generator 会引入 tokenizer、输入条件、数据格式和训练目标差异，反而不公平。

V4 最现实、最干净的 baseline 是 fair internal baseline：

> FairIntra-BL：使用同一 frozen PulpMotion Stage1 latent、同一 DiT backbone、同一数据 split、同一训练步数、同一 sampler，分别训练三个独立 diffusion model；每个模型只负责一个任务，不使用 branch-mask unified training。

三条 baseline：

| baseline             | 任务                | 输入                      | 输出                    | 对照目的                                                                       |
| -------------------- | ----------------- | ----------------------- | --------------------- | -------------------------------------------------------------------------- |
| FairIntra-BL-Joint   | joint generation  | text                    | human + camera latent | 判断 unified model 的 joint 性能是否因多任务训练退化                                      |
| FairIntra-BL-CamComp | camera completion | text + GT human latent  | camera latent         | 判断 unified model 的 camera completion 是否真正强                                 |
| FairIntra-BL-HumComp | human completion  | text + GT camera latent | human latent          | 判断 unified model 的 human completion 低 TMR 是任务本身、模型耦合还是 unified training 问题 |

报告时可写：

```text
We construct fair internal baselines by training separate diffusion models for each conditional generation task, using the same frozen tokenizer, backbone, data splits, training budget, and sampling protocol, but without the branch-mask unified training mechanism.
```

### 4.2 Baseline 公平性约束

必须固定：

1. Frozen PulpMotion Stage1 tokenizer。
2. 数据 split：mixed full 10549 与 pure full 4053 的定义不变。
3. latent 表示和 decode/evaluator pipeline 不变。
4. Stage2 backbone 容量尽量一致；若 separate model 总参数量为 unified 的约三倍，需要同时报告 single-model params 与 total params。
5. sampling steps、cfg/eta 搜索范围一致。
6. 指标和 render gate 一致。

### 4.3 Completion 任务的公平指标

Camera completion：

| 指标组 | 必须报告 | 解释 |
| --- | --- | --- |
| Camera semantic | FDCLaTr、CLaTr-Score、R3、F1、Camera Coverage | 相机轨迹与 caption / reference distribution 的语义质量 |
| Projection geometry | FDframing、Out-rate、in-frame ratio、bbox scale/center error | 相机是否把给定 human 拍好 |
| Temporal reliability | camera jitter、projection jitter | 是否出现不可用相机运动 |
| Visual evidence | GT human under generated camera projection | 直接展示“给定动作，补相机”的应用价值 |

Human completion：

| 指标组                    | 必须报告                                                        | 解释                                                 |
| ---------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| Human distribution     | FDTMR、TMR-Score、R3、Human Coverage                           | 保留 official metric，但承认 TMR 是 text-retrieval biased |
| Camera-conditioned fit | GT camera projection in-frame ratio、bbox consistency        | 人体是否适配给定 camera                                    |
| Motion quality         | MPJPE to GT、contact proxy、foot skating proxy                | 防止只靠 coverage 掩盖动作质量                               |
| Sensitivity            | text shuffle、camera latent shuffle、camera latent zero/noise | 解释低 TMR 与 condition reliance                       |

### 4.4 Completion 应用可视化

V4 需要明确 completion 的应用场景，而不是只报表：

1. **Camera director mode**：给定 human motion，自动补 cinematic camera。展示 GT human fixed skeleton、GT camera projection、StoryMotion camera completion projection、FairIntra-BL projection。
2. **Actor recovery mode**：给定 camera path 和 text，补全 human motion。展示 GT camera 下 GT human、StoryMotion human completion、FairIntra-BL human completion。
3. **Interactive editing mode**：保持 human 不变，修改 text 或 camera condition，观察 camera/human 分支是否按任务变化。

最小 demo set：10 个成功样本 + 10 个困难样本。困难样本要主动展示 failure taxonomy，而不是只挑好看结果。

---

## 5. Joint Mode Human 质量下降：假说与验证

### 5.1 当前问题

用户指出的样例：

```text
linkedCodebases/StoryMotion/stage2/bilateral_cfg_pulpmotion_fair_compare_20260615/bi_h1.0_c3.0_eta0.0/2011_-4GsCEopbd4_00008_001_a/story_human_vs_joint_concat.mp4
```

现象：human completion 与 joint generation 使用同一模型、同一 latent space，但 joint 下 human motion 质量更差。直觉上 human 与 camera generation 应该相对独立；如果有依赖，也应是 camera 对 human 有依赖，而不是 joint human 因 camera branch 生成而显著变差。

V4 判断：这个直觉需要修正。当前 evidence 已经显示 human completion 对 observed camera latent 强依赖，说明模型学到的是强 human-camera coupling。Joint mode 同时生成 human 与 camera 时，camera latent 本身也是生成结果；如果生成 camera latent 分布偏差、human-camera cross-attention/latent coupling 过强、或 text condition 被弱化，就可能把 human branch 拉向低质量或低语义区域。

### 5.2 候选根因

| 假说                                               | 机制                                                                                  | 已有证据                                                 | 需要验证                                                                     |
| ------------------------------------------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------ |
| H1: Generated camera latent 分布偏差污染 human branch  | joint 中 camera 不是 GT observed，而是模型同时生成；错误 camera latent 通过 latent coupling 影响 human | human completion 对 camera latent zero/shuffle 强敏感    | 用 GT camera 替换 generated camera 的 hybrid sampling                        |
| H2: Text condition 在 human branch 中被弱化           | 模型主要依赖 camera latent，text 只提供弱全局约束                                                  | zero/shuffle camera-text half 几乎不变；standard CFG 扫描无效 | text shuffle / text zero 在 joint 与 human completion 的 sample-level delta |
| H3: 多任务训练造成 branch gradient conflict             | camera completion、human completion、joint 的 target mask loss 竞争                      | long training 不能自然解决；不同 checkpoint 指标 tradeoff 明显    | separate FairIntra-BL 与 unified 对比                                       |
| H4: START_X latent MSE 优先拟合 easy camera geometry | latent loss 与 TMR/retrieval semantic 不一致                                            | Stage1 upper bound 高于 Stage2；joint semantic 指标不全面支配  | 加 text-alignment auxiliary 或 selection-by-render/TMR gate                |
| H5: Evaluator-task mismatch                      | human completion 是 conditional task，TMR 是 text-only retrieval metric                | high coverage + low TMR 同时出现                         | GT oracle completion 与 text-shuffle 对照                                   |

### 5.3 优先实验

Priority 0：只做诊断，不急着改模型。

1. **Hybrid GT-camera test**：在 human completion 中给 GT camera，已知是当前 setting；再构造 joint-like pipeline：先 joint 生成 camera，再固定该 camera 生成 human；最后用 GT camera 替换 generated camera 生成 human。若 GT camera 版本 human 指标显著更好，H1 成立。
2. **Generated-camera replay**：把 joint 生成出的 camera latent 作为 observed branch 输入 human completion，生成 human。比较 joint human 与 replay human。如果 replay human 明显好于 joint human，问题在 simultaneous joint denoising；如果同样差，问题在 generated camera latent 质量或 camera-human coupling。
3. **Text intervention**：在 GT camera、generated camera、shuffled camera 三种条件下做 text zero/shuffle。若 human 变化仍小，H2 成立。
4. **FairIntra-BL-HumComp 对比**：若 separate human completion 的 TMR 明显高于 unified human completion，H3 成立；若同样低，说明任务/evaluator 本身是主因。
5. **Projection render audit**：对上述四组都输出 camera projection，检查 low TMR 是否对应视觉失败，还是只是 retrieval semantic mismatch。

### 5.4 可能修复路线

不建议把“调 human/camera/joint loss 比例”当成主要解决方案。比例扫描有诊断价值，但它很容易产生伪缓和：某一分支质量下降后，cross-branch delta 变小，看起来像解耦，实则是 branch collapse 或简单 tradeoff。

比例扫描应按以下方式设计：

| 扫描对象 | 诊断指标 | 真缓和信号 | 伪缓和信号 |
| --- | --- | --- | --- |
| human/camera/joint task sampling ratio | joint human/camera official metrics、completion metrics、projection stats | human 与 camera 质量都不下降，intervention delta 下降，projection render 更稳定 | 某分支 coverage/FDTMR/FDCLaTr 崩掉，delta 下降只是因为分支被忽略 |
| branch loss weight | per-branch loss、official metrics、generated-camera replay gap | replay gap 变小且 branch quality 保持 | 指标沿单调 tradeoff 线滑动，没有 Pareto 改善 |
| observed-branch dropout/noise ratio | text intervention delta、observed latent intervention delta | text delta 上升、latent perturbation delta 适度下降、completion quality 不崩 | completion fit 下降，camera-conditioned/human-conditioned 应用价值丢失 |
| branch-specific CFG ratio | TMR/CLaTr、FDframing/Out-rate、projection jitter | semantic 指标改善且 geometry/render 不退化 | 只提高语义分数但投影离屏或相机质量下降 |

短期不建议把 MINE/互信息等难以稳定估计的量作为 P0 证据。P0 用更可复现的污染指数：

```text
PI_H<-C = degradation(human metric | camera branch perturbed) - degradation(human metric | no perturb)
PI_C<-H = degradation(camera metric | human branch perturbed) - degradation(camera metric | no perturb)
```

其中 perturbation 使用 same-seed generated branch replay、shuffle、zero、noise-matched 四类；成功不是 PI 单独下降，而是 PI 下降同时 branch absolute quality、coverage、projection metrics 不明显退化。

不靠简单调比例的机制路线如下。文献启发来自 [[analysis/CVPR_2024/MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Latent_Diffusion_Model|MCM-LDM]] 的主/辅条件优先级与 AdaLN-Zero 动态注入、[[analysis/NEURIPS_2023/FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing|FineMoGen]] 的稀疏专家/时空解耦、[[analysis/arxiv_2023/VideoComposer_Compositional_Video_Synthesis_with_Motion_Controllability|VideoComposer]] 的文本/空间/时间条件分解与统一时空条件编码，以及 [[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]] 的两阶段去噪调度。

先按最小干预排序：

| 修复 | 具体做法 | 成功判据 | 风险 |
| --- | --- | --- | --- |
| Two-stage denoising isolation | 推理早期隔离 human/camera 分支交互，后期恢复 cross-branch 交互；扫描 boundary 0.4/0.5/0.6/0.7 | PI 降低 30% 以上，joint human/camera official metrics 与 projection render 不退化 | 过晚恢复交互会导致 human-camera 不协调 |
| Branch-specific CFG / channel gating | human branch 与 camera branch 分开 CFG；joint 下提高 human text CFG、降低 camera coupling | TMR +5% 以上，FDframing/Out-rate 不退化超过 10% | 可能破坏 geometry |
| Camera latent dropout during human target training | 训练时对 observed camera latent 做小概率 zero/noise/dropout，强制 text 保留控制力 | human completion TMR 上升，camera perturbation delta 降低但 coverage 不崩 | 可能削弱 camera-conditioned fit |
| Task-balanced or branch-balanced loss | 调整 human/camera/joint loss 权重，减少 easy camera branch 主导 | joint TMR 与 render gate 改善 | 可能损失 camera completion |
| Confidence-gated cross-branch injection | 在 branch 融合处加轻量 confidence head，用当前预测误差/branch feature 估计信任度，低置信分支减少向对方注入 | PI 降低 40% 以上，无扰动 joint 质量下降不超过 2% | gate 饱和后可能把有用交互也关掉 |
| Sparse branch expert / MoE routing | 参考 FineMoGen，把 human-only、camera-only、joint-interaction 作为稀疏专家 | 对冲突样本提升明显，正常样本不退化 | 工程量较大，P0 不做 |
| Text-alignment auxiliary | 对 decoded human 引入轻量 semantic selection / auxiliary loss | TMR 提升且 raw skeleton 不退化 | 工程复杂，需避免伪造 evaluator shortcut |
| Two-stage joint sampling | 先生成 human，再 condition camera；或先生成 camera 后 human replay | human quality 与 projection 同时提升 | 可能削弱“一次性 unified generation”叙事 |

V4 推荐优先顺序：

1. **P0 generated-camera replay + GT-camera oracle**：先确认 joint human 下降来自 simultaneous denoising 还是 generated camera 条件质量。
2. **P0 two-stage denoising isolation**：纯推理改动，不需重训。若有效，说明 early cross-branch contamination 是关键因素。
3. **P1 confidence-gated cross-branch injection**：需要小模块和微调，但能把“预测较差的 branch 不污染另一 branch”变成明确机制。
4. **P1 branch-specific CFG / channel gating**：作为低成本修复与 ablation，不作为唯一机制贡献。
5. **P2 MoE routing / priority AdaLN-Zero**：若 P0/P1 证明有必要，再做结构化版本。

---

## 6. 下一批实验矩阵

### 6.1 最小闭环清单

| 优先级 | 实验                                      | 目的                                                                 | 输出路径                                                                                  | 成功判据                                                                                                 | 失败判据                                  |
| --- | --------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------- |
| P0  | Human-in-camera-projection render gate  | 验证 geometry 指标是否对应视觉可靠性                                            | `stage2/vis/{joint,camera_completion,human_completion}/...` 与 `stage2/metrics/...`    | 至少 100 samples 无系统性投影错误；in-frame ratio、bbox jitter、projection outlier rate 支持 StoryMotion 优势         | 出现大量离屏、抖动、反向投影或 render convention 不可信 |
| P0  | Metrics/vis 目录重整                        | 防止证据继续散落在 stage2 根目录                                               | `stage2/vis/`、`stage2/metrics/`                                                       | 新实验所有输出按 mode/method/run_id 归档                                                                       | 指标和渲染仍混放，无法复现                         |
| P0  | Generated-camera replay                 | 判断 joint human 下降是 simultaneous denoising 还是 generated camera 条件问题 | `stage2/metrics/joint/diagnostics/generated_camera_replay/`                           | replay/GT-camera 能解释 joint human 差距                                                                  | 替换 GT camera 后仍差，说明根因不在 camera 条件     |
| P1  | FairIntra-BL-CamComp                    | completion baseline 核心                                             | `stage2/metrics/camera_completion/fair_intra_bl/`                                     | StoryMotion camera completion 在 FDCLaTr、coverage、projection metrics 上优于或不弱于 separate baseline，同时参数更省 | separate baseline 明显更强，统一框架贡献受损       |
| P1  | FairIntra-BL-HumComp                    | 解释 human completion TMR                                            | `stage2/metrics/human_completion/fair_intra_bl/`                                      | 若 baseline 同样低 TMR，支持 task/evaluator mismatch；若 StoryMotion 更低，定位 unified training 问题                | 无法解释 low TMR，且视觉也差                    |
| P1  | Branch-mask vs separate-task 消融         | 支撑统一框架贡献                                                           | `stage2/metrics/ablation/branchmask_vs_separate/`                                     | unified 三任务平均性能不显著低于 separate，参数/训练成本更低                                                              | unified 明显牺牲关键任务                      |
| P1  | Text/camera sensitivity full-set        | 形成诊断贡献                                                             | `stage2/metrics/diagnostics/condition_sensitivity/`                                   | camera latent perturbation 与 text perturbation 的 delta 排序稳定，解释 completion 行为                         | delta 不稳定或与主张矛盾                       |
| P1  | Ratio scan as diagnosis                 | 判断 latent 耦合是否随 task/loss/dropout 比例缓和                             | `stage2/metrics/diagnostics/ratio_scan/`                                              | PI 降低且 human/camera absolute quality、coverage、projection metrics 不退化                                 | PI 降低来自 branch collapse 或单调 tradeoff  |
| P1  | Two-stage denoising isolation           | 零训练成本验证 early cross-branch contamination                           | `stage2/metrics/joint/two_stage_isolation/` 与 `stage2/vis/joint/two_stage_isolation/` | PI 降低，joint metrics 与 projection render 不退化                                                          | human-camera 协同变差或 boundary 敏感        |
| P2  | Branch-specific CFG                     | 低成本修复 joint human                                                  | `stage2/metrics/joint/branch_cfg/`                                                    | TMR 提升且 FDframing/Out-rate/render gate 不明显退化                                                         | TMR 不动或 geometry 崩                    |
| P2  | Camera dropout fine-tune                | 训练期缓解过依赖 camera latent                                             | `stage2/metrics/joint/camera_dropout_ft/`                                             | human TMR/render 改善，camera completion 不显著退化                                                          | completion 优势丢失                       |
| P2  | Confidence-gated cross-branch injection | 防止低置信分支污染另一分支                                                      | `stage2/metrics/joint/confidence_gate/`                                               | PI 降低 40% 以上，无扰动质量下降不超过 2%                                                                           | gate 饱和、协同信息被过度抑制                     |

### 6.2 论文级成功标准

最低可投稿标准：

1. Joint mode：保留 V3 在 FDframing、Out-rate、FDTMR、coverage 上的优势，且补齐 100-sample camera-projection render gate。
2. Camera completion：相对 FairIntra-BL-CamComp 至少在 camera semantic 或 projection reliability 上有明确优势，或者在性能接近时以单模型三任务覆盖和参数效率取胜。
3. Human completion：即使 TMR 低，也必须通过 FairIntra-BL、oracle GT camera、text/camera intervention 证明低 TMR 的来源，并用 projection render 证明可用边界。
4. Unified framework：相对 three separate models，在总参数量/训练成本上明显更优，且三任务平均性能不显著下降。
5. Reliability：所有正式结论都有 `metrics` JSON/CSV 与 `vis` MP4 对应证据，路径稳定且可复现。

不能接受的状态：

1. 只有 aggregate metric，没有 projection render。
2. Completion 没有 same-task baseline。
3. Human completion low TMR 只用口头解释，没有 oracle/intervention 证据。
4. Joint human 质量下降样例仍无法定位原因。
5. 新结果继续散落在根目录，无法追踪 run meta。

---

## 7. V4 贡献草案

如果下一批实验成功，论文贡献可写成三点：

1. **Unified branch-mask latent diffusion for human-camera generation**：提出基于 frozen continuous human/camera tokenizer 的 branch-mask Stage2 diffusion，用一个模型统一支持 joint generation、camera completion 与 human completion。
2. **Strong joint generation gains over PulpMotion in geometry and coverage**：在 PulpMotion official full-test evaluator 上，StoryMotion 在 camera-human geometry、FDTMR、Human Coverage 与 Camera Coverage 上显著优于 PulpMotion matrix，同时诚实报告 semantic 指标的非全面支配。
3. **Fair conditional completion benchmark and reliability protocol**：构建 human-camera completion 的 fair internal baselines、条件依赖诊断与 human-in-camera-projection reliability protocol，证明 camera completion 的应用优势，并解释 human completion / joint human quality 的条件耦合与失败边界。

如果 joint human 修复成功，可把第三点升级为：

> 系统性揭示并缓解 multi-branch joint diffusion 中的 conditional dominance：通过 generated-camera replay、text/camera intervention 与 branch-specific guidance/dropout，定位 camera latent 对 human branch 的过强支配，并在不破坏 geometry 的情况下改善 joint human semantic alignment。

如果修复失败，则第三点保持为 benchmark/protocol contribution，不声称解决 conditional dominance。

---

## 8. 当前行动顺序

1. **先做 projection render gate**：从已有 corrected fair-compare sample 扩展到 100 samples，统一输出到 `stage2/vis/` 与 `stage2/metrics/`。这是高优先级可靠性门槛。
2. **再做 generated-camera replay 与 GT-camera oracle**：直接回答为什么 joint 下 human 质量下降。
3. **补齐 full-set dependency matrix**：human-text、all-text、camera completion 对称实验、observed latent zero/shuffle/noise 与 sample-level delta。
4. **做 two-stage denoising isolation**：先用纯推理调度验证 early cross-branch contamination 是否成立。
5. **并行启动 FairIntra-BL-CamComp 与 FairIntra-BL-HumComp**：这是 completion 贡献能否成立的关键。
6. **根据诊断结果选择修复**：若 two-stage isolation 正面，再做 confidence gate；branch-specific CFG 作为低成本 ablation，而不是最终机制。
7. **最后整理论文叙事**：只声明已被 metrics、render 与 baseline 同时支撑的贡献。

---

## 9. 证据路径

V3 正式指标：

- `linkedCodebases/StoryMotion/stage2/pulpmotion_official_matrix_20260616/full/`
- `linkedCodebases/StoryMotion/stage2/p1_parallel_20260615/indepdrop_joint_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/stage2/p1_parallel_20260615/indepdrop_camera_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/stage2/p1_parallel_20260615/indepdrop_human_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/stage2/p1_parallel_20260615/puretrain_camera_pure_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/stage2/p1_parallel_20260615/puretrain_human_pure_full_cfg2.0_eta1.0.json`
- `linkedCodebases/StoryMotion/stage2/v3_closure_20260616/full/`
- `linkedCodebases/StoryMotion/stage2/v3_closure_20260616/completion_ablation/`
- `linkedCodebases/StoryMotion/stage2/v3_closure_20260616/latent_block_gate/`
- `linkedCodebases/StoryMotion/stage2/human_completion_dependency_20260617/human_text_zero_camera_full.json`
- `linkedCodebases/StoryMotion/stage2/human_completion_dependency_20260617/human_text_shuffle_camera_full.json`
- `linkedCodebases/StoryMotion/stage2/human_completion_dependency_20260617/human_camera_latent_zero_full.json`
- `linkedCodebases/StoryMotion/stage2/human_completion_dependency_20260617/human_camera_latent_shuffle_full.json`

V3 渲染与 raw-skeleton gate：

- `linkedCodebases/StoryMotion/stage2/joint_channel_gated_pulpmotion_fair_compare_20260615/manifest.json`
- `linkedCodebases/StoryMotion/stage2/gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616/manifest.json`
- `linkedCodebases/StoryMotion/stage2/v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare/manifest.json`
- `linkedCodebases/StoryMotion/stage2/v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare/manifest.json`
- `linkedCodebases/StoryMotion/stage2/native_projection_fair_compare_20260617/manifest.json`

V4 新增输出目标：

- `linkedCodebases/StoryMotion/stage2/vis/`
- `linkedCodebases/StoryMotion/stage2/metrics/`

2026-06-18 4090 smoke：

- `linkedCodebases/StoryMotion/stage2/vis/v4_projection_split_smoke_20260618/source/`
- `linkedCodebases/StoryMotion/stage2/metrics/v4_projection_split_smoke_20260618/source/`
- `linkedCodebases/StoryMotion/stage2/vis/v4_projection_split_smoke_20260618/fair_compare/`
- `linkedCodebases/StoryMotion/stage2/metrics/v4_projection_split_smoke_20260618/fair_compare/`
- `linkedCodebases/StoryMotion/runs/eval/stage2/v4_dependency_smoke_20260618_s128/summary_all_s128.json`

相关状态：

- 5090 `/data` 于 2026-06-17T16:33+08:00 出现介质级读错误，运行中 Stage1 mixed full、human text zero-human、human camera-latent noise-matched 等作业未形成完成结论；恢复前不得把这些 partial job 写成结果。详见 [[2026-06-17_storymotion-5090-sda-failure-rescue]]。

---

## 10. Human-Camera 双分支解耦生成与控制机制

本节回应 poool note 中的 StoryMotion 任务：如何在现有 `z = concat([z_hum, z_cam])` 与 branch-mask Stage2 diffusion 上解耦 human / camera 双分支，减少互相损害，同时把 screen projection 从生成机制降级为可靠性评估 gate。

参考机制来自 [[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories|Motion Prompting]]、[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]、[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence|PoseAnything]]、[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]、[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]、[[analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance|DanceCamera3D]]、[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]、[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]] 与 [[analysis/arxiv_2023/VideoComposer_Compositional_Video_Synthesis_with_Motion_Controllability|VideoComposer]]。本节只给出设计与诊断计划，不把任何未跑实验写成结果。

### 10.1 问题定义

目标不是让 human 与 camera 完全独立。电影式人-相机生成需要三类信息同时成立：

1. **分支私有可控性**：human branch 应主要承担人体语义、pose、contact、motion quality；camera branch 应主要承担轨迹、镜头语义、速度、构图节奏。
2. **投影可靠性可验证**：两分支必须在屏幕投影、bbox scale、in-frame ratio、framing jitter 等后验几何上可检验，否则会回到 PulpMotion / DanceCamera3D 所指出的出画和糟糕取景问题；但这些 projection stats 不能成为 Stage2 的核心生成桥。
3. **故障隔离**：joint mode 中 generated camera latent 若质量差，不应无门槛污染 human branch；generated human latent 若异常，也不应无门槛拖坏 camera branch。
4. **human 优先原则**：无论是否给 camera，human branch 的固定视角动作质量、骨架动力学和文本语义都不能被 camera branch 降低；camera-projection render 只能验证“生成结果在镜头里是否可用”，不能替代 raw human motion quality。

因此 V4 的解耦定义为：

> human / camera 在 private latent 与 text condition 上尽量隔离；projection 只作为后验 render / metrics gate；任何跨分支信息交换都必须经过可消融的显式 gate 或 staged schedule，而不是通过 concat latent 的无限制交互传播。

### 10.2 为什么当前 branch-mask / latent 拼接可能互相损害

当前 StoryMotion 把 `z_hum` 与 `z_cam` 拼接后送入同一个 Stage2 diffusion，再用 branch mask 区分 joint、camera completion 与 human completion。这个设计带来统一三任务能力，但也埋下三个风险：

1. **条件优先级偏移**：已有 human completion intervention 显示，zero/shuffle camera-text half 几乎不变，而 zero/shuffle observed camera latent 会导致 human 指标大幅退化。这说明模型在当前设置下更依赖 observed camera latent，而不是 camera text half。
2. **generated branch 污染**：human completion 中 observed camera 是 GT latent；joint mode 中 camera latent 同时由模型生成。如果 generated camera 偏离数据分布，human branch 可能把错误 camera latent 当作强条件使用，造成 joint human 质量下降。
3. **branch-mask 只定义任务，不定义信息边界**：mask 告诉模型哪个 branch 是 observed / target，但没有限制 hidden state、self-attention 或 residual mixing 中的跨分支传播。换言之，branch-mask 是任务接口，不是解耦机制。

这也是为什么“只调 human/camera loss 比例”不够：比例扫描可能只是让某一分支变弱，从而降低 cross-branch delta，看起来像解耦，实际可能是 branch collapse。

### 10.3 Video Control 工作的可迁移机制

以下借鉴不直接复制 video 模型结构，而是抽取可迁移的控制原则：

| 工作               | 可迁移原则                                                                                    | 对 StoryMotion 的启发                                                          |
| ---------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Motion Prompting | 用点轨迹和可见性作为统一 motion prompt，密集训练可泛化到稀疏推理，但组合物体与相机运动会出错                                    | 控制信号应显式化为轨迹 / projection 统计；组合控制必须有冲突诊断                                    |
| MotionCtrl       | camera pose 进入 temporal transformer，object trajectory 进入 spatial convolution，按运动属性选择注入位置 | human / camera 条件不应只做通道拼接，应分配到分支专用路径                                       |
| PoseAnything     | 主体与相机用 decoupled CFG 分开注入；部件级 attention 把全局一致性拆成局部控制                                     | StoryMotion 可优先做 branch-specific CFG、condition 置空 / 交换诊断，再考虑 branch 专用 adapter |
| ActCam           | 早期深度+姿态锁全局结构，后期仅姿态保留细节；全程强深度会过约束                                                         | joint denoising 可做 early branch isolation 与 late limited residual，不把 projection 作为训练桥 |
| DanceCamera3D    | 用 body attention loss 和 DMR/LCD 检查人物是否被相机捕捉；dance/music CFG 分离显示不同条件权重的 trade-off           | StoryMotion 可借鉴 human-in-camera projection 指标和可视化协议，但不把它改成 Stage2 生成机制 |
| E.T. / Director  | 全局坐标和角色轨迹显式条件优于角色相对简化；cross-attention 保留完整时空条件序列                                         | camera branch 需要显式读取 human trajectory / projection summary，而不是只依赖混合 latent |
| COIN             | 动态控制信号、软修复、人-场景深度关系损失提供独立几何约束                                                            | gate 应按 confidence、branch perturbation delta 与 projection error 动态调节，不应固定全开 |
| VideoComposer    | 文本、空间、时间条件分解后用统一 STC encoder 聚合；冲突处理仍是开放问题                                               | StoryMotion 应分解 text / human / camera / projection 条件，并显式报告冲突失败            |

### 10.4 Human-Camera 解耦设计收敛

经 DeepSeek max 严肃质询后，方案收紧为三层，不把所有模块同时塞进 P0：

| 层级  | 定位        | 模块                                                                                                    | 当前结论                             |
| --- | --------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| P0  | 最小可做、验证假设 | PoseAnything-inspired branch-specific CFG、channel-gated CFG、two-stage denoise isolation、intervention diagnostics、camera-projection render gate | 优先做；无需重构主干，能验证过耦合是否来自采样 / 条件优先级 / generated branch 污染 |
| P1  | 轻量训练模块    | 分支专用条件通道、cross-branch residual gate、branch-specific condition adapter                                | 作为可训练修复；必须有 fixed-open / fixed-closed / no-gate 对照 |
| P2  | 大改或高风险    | MI / orthogonal private-shared 分解、token-level masked attention、自适应调度网络                                | 先不承诺为 V4 核心；只有 P0/P1 证明需要时再做     |

被否掉或收紧的点：

1. **否掉“只分 text 通道就等于解耦”**：若 latent concat 后仍无限制交互，text lane 分开只能改善 text utilization，不能证明 human-camera latent 污染已解决。
2. **收紧 MI / orthogonal 约束**：它不能直接压在完整 `z_hum` 与 `z_cam` 上，否则会和 human-camera 协同需求冲突；最多用于 private 子空间，且属于 P2。
3. **收紧 residual gate**：gate 可能只是 attention mask 的软版本；必须和 fixed-open、fixed-closed、no-gate 做消融，不能直接写成贡献。
4. **删除 Projection Consistency Bridge 作为模块**：Stage1 已经基于 PulpMotion，Stage2 若再引入 PulpMotion-style bridge 会被认为是增量，且会把优化重心压到 camera projection 内的人体，忽视 projection 外的 human motion。V4 只保留 projection render / metrics 作为 evaluation gate，不把它作为训练或采样桥。

### 10.5 可实现模块设计（删除 Projection Bridge 版）

这里把“实验优先级”和“最终方法贡献优先级”分开。已有代码能马上运行的 P0 是诊断与采样；论文贡献若要成立，最终仍需要证明结构性 no-degradation，而不能只靠 CFG 或投影后处理。

更稳的写法是两层框架，而不是“先诊断、后补丁”：

1. **Tier-1 / training-free decoupling guidance**：branch-specific CFG、channel-gated CFG、text / latent intervention 与 replay / oracle 共同构成低成本解耦引导与因果诊断层。若它有效，只能写成 training-free guidance contribution，不能写成 latent 已完全解耦。
2. **Tier-2 / trainable structural decoupling**：branch-specific condition adapter 与 cross-branch residual gate 是结构性 no-degradation 的候选核心贡献。至少需要一个轻量配置的真实训练或严格 ablation，否则 ICLR 贡献会偏弱。
3. **Projection render gate / optional safety**：只作为 post-hoc safety 与可视化可靠性检查，不作为 joint generation 的默认回退逻辑，更不能用来掩盖 camera control 失败。

**模块 A：分支专用条件通道 / Adapter**

将 text condition 显式拆成 human lane 与 camera lane：

```text
c_text -> c_h = Adapter_h(c_text)
       -> c_c = Adapter_c(c_text)

human denoise path: z_h, c_h
camera denoise path: z_c, c_c
```

该模块与 PoseAnything 的关系是“条件可分离注入”的间接借鉴，不是复用其架构。PoseAnything 证明 subject / camera 条件不能总用一个耦合 CFG 处理；StoryMotion 的对应问题是 human-text、camera-text、observed-human latent、observed-camera latent 必须能分别置空、交换和缩放。

当前排序：

1. **实验 P0**：先用已有 `--text-intervention` 和 `--channel-gated-cfg` 验证条件 lane 是否值得做成训练结构。
2. **方法 P1 / 候选核心贡献**：若诊断显示 text lane 和 latent dominance 明确存在，再训练轻量 branch-specific adapter，并与 no-adapter 对照。

重要边界：Module A 单独不能宣称解耦；它只能证明 condition path 更清晰。真正的 no-degradation 必须看 human-only、human completion、joint human 在 fixed-view quality 和 projection render 上是否同时不退化。

**模块 C：Cross-Branch Residual Gate**

如果需要跨分支交互，用显式 residual gate 控制，而不是每个 block 无门槛互读：

```text
z_h' = z_h + g_h<-c(t, q_c, d_c) * F_c->h(z_c)
z_c' = z_c + g_c<-h(t, q_h, d_h) * F_h->c(z_h)
```

其中 `q_h/q_c` 是分支置信度 proxy，`d_h/d_c` 是 intervention delta 或 predicted-x0 稳定性 proxy。projection error 可以作为 gate trace 的解释变量，但不作为训练输入桥。

必须消融：

1. gate 恒为 0：完全隔离。
2. gate 恒为 1：无门控残差。
3. learned gate：动态门控。
4. no-gate baseline：当前 branch-mask。

若 learned gate 不优于固定策略，就不能把 gate 写成核心贡献。

**模块 D：Private / Shared 诊断，而非主训练目标**

不建议直接对完整 `z_h` 与 `z_c` 做低互信息或正交约束。当前只做诊断性版本：

```text
measure: CCA / SVCCA / linear probe / perturbation delta
scope: branch-private residual features, not full latent
claim: diagnostic only, no causal disentanglement claim
```

该模块属于 P2。只有当 Module A / C 与 sampling-time CFG 都无法解释 human degradation 时，再考虑 token-level masked attention 或 private-shared latent decomposition。

**模块 E：Branch-Specific CFG 与 Two-Stage Denoise Schedule**

这是最明确参考 PoseAnything 的部分，优先级应提高为 **实验 P0**，但写作上只能称为 sampling-time diagnosis / guidance，不应称为结构性解耦。

现有可执行版本：

1. branch-specific CFG：joint mode 中分别扫描 `cfg_h` 与 `cfg_c`。
2. channel-gated CFG：只把 human text guidance 写回 human latent channels，只把 camera text guidance 写回 camera latent channels。
3. text intervention：`zero_human`、`zero_camera`、`shuffle_human`、`shuffle_camera`。
4. latent intervention：completion 下对 observed branch 做 `zero`、`shuffle`、`noise_matched`。

推荐的 StoryMotion CFG 形式应优先使用 unconditional anchor 与 channel mask，而不是照搬 PoseAnything 的 camera-only baseline 减法：

$$
\epsilon=\epsilon_{\emptyset}+w_h P_h(\epsilon_h-\epsilon_{\emptyset})+w_c P_c(\epsilon_c-\epsilon_{\emptyset})
$$

其中 $P_h/P_c$ 是 human / camera latent channel mask。这个形式更符合 StoryMotion 的 `z=concat([z_h,z_c])`，也更容易和 `--channel-gated-cfg` 对齐。

two-stage denoise isolation 不应再写成 early projection-only。新的定义是：

```text
early timesteps: branch-private or channel-gated denoise, suppress full latent exchange
late timesteps: restore standard joint denoise or limited residual gate
```

它的作用是检测 early cross-branch contamination，不是引入新的 projection mechanism。

**模块 F：Camera-Projection Render Gate（评估-only）**

这不是方法模块，也不是训练损失。它只在生成后运行：

```text
decode human + camera
project joints under GT / generated camera
render camera_projection.mp4
compute in-frame ratio, fully-in-frame ratio, bbox jitter, behind-camera ratio
```

成功标准必须双视角成立：

1. fixed-view human skeleton 不退化。
2. camera-projection render 不出现系统性出画、反向投影、bbox 抖动或不可解释失败。

DanceCamera3D 的 DMR/LCD 和 body attention loss 可以借鉴为指标概念；PulpMotion 的 FDframing / Out-rate 可以借鉴为几何评估；但 V4 不训练 projection loss，不训练投影预测器，也不把 projection 作为 Stage2 共享通道。

### 10.6 训练、推理与评估流程

**P0 诊断 / 采样流程**

1. 保持 Stage1 tokenizer、Stage2 backbone 与 branch-mask checkpoint 不变。
2. 跑 branch-specific CFG grid：`cfg_h/cfg_c` 小范围扫描，保持 sampler、checkpoint、split 不变。
3. 跑 channel-gated CFG：验证 PoseAnything-style condition separation 在 concat latent 上是否有效。
4. 跑 text / latent intervention：区分 text lane 弱化、observed latent dominance 和 generated branch 污染。
5. 对同一批样本输出 official metrics、fixed-view skeleton render、camera-projection render、per-sample delta 和 failure taxonomy。

**P1 结构训练流程**

1. 加 branch-specific condition adapter，初始化为接近原共享投影，避免一开始破坏 checkpoint 行为。
2. 加 cross-branch residual gate，但 gate 初始偏向小 residual；先验证 fixed-open / fixed-closed。
3. 不加入 projection loss，不加入 projection prediction head。
4. 训练只报告和同 checkpoint / same split / same sampler 对齐的结果，不与早期 smoke 或 partial job 混合解释。

**推理流程**

1. 输入 text，生成 `c_h` 与 `c_c`。
2. joint mode 用 branch-specific / channel-gated CFG 采样。
3. 若实现 residual gate，只在 late denoise 或高置信分支中开放有限 residual。
4. 采样结束后 decode human / camera，先看 fixed-view human，再看 camera-projection render。
5. 对失败样本保留 same-seed intervention：generated-camera replay、GT-camera oracle、shuffle/noise observed latent。

### 10.7 消融与诊断矩阵

| 编号  | 设置                                         | 目的                                                           | 必须看                                                              |
| --- | ------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------------- |
| A0  | current branch-mask baseline               | 复现现有强弱项                                                      | official metrics + fixed-view render + projection render         |
| A1  | branch-specific CFG only                   | 判断分支 guidance 是否有 Pareto 区间                                  | TMR、CLaTr、FDframing、Out-rate、human fixed-view quality            |
| A2  | channel-gated CFG                          | 验证 guidance 是否应限制在对应 latent channels                         | human/camera 指标是否同时不退化                                           |
| A3  | text intervention matrix                   | 区分 text lane 弱化和 latent dominance                            | zero / shuffle human-text、camera-text、all-text                   |
| A4  | observed-latent intervention               | 测 camera latent 对 human 的污染曲线                                | zero / shuffle / noise-matched observed branch                   |
| A5  | generated-camera replay + GT-camera oracle | 判断 joint human 下降来自 generated camera 还是 simultaneous denoise | replay human vs joint human vs oracle human                      |
| A6  | two-stage denoise isolation                | 判断 early contamination 是否存在                                  | generated-camera replay gap、fixed-view quality、projection jitter |
| A7  | branch-specific condition adapter          | 分离 text lane 是否有效                                            | text intervention delta 下降且 absolute quality 不降                  |
| A8  | residual gate                              | 验证动态交互是否必要                                                   | fixed-open / fixed-closed / learned gate                         |
| A9  | private-shared diagnostic                  | 只做相关性诊断，不做主张                                                 | CCA / perturbation delta                                         |

必须补齐的 intervention：

1. **human branch sensitivity**：GT camera、generated camera、shuffled camera、noise-matched camera 下的 human metrics、fixed-view render 与 projection render。
2. **camera branch sensitivity**：GT human、generated human、shuffled human、noise-matched human 下的 camera metrics 与 projection render。
3. **same-seed replay**：joint generated camera replay 到 human completion；GT-camera oracle 替换；比较 joint human 与 replay human。
4. **branch text intervention**：zero/shuffle human-text、camera-text、all-text，区分 text lane 弱化和 latent dominance。
5. **gate trace**：若使用 learned gate，记录每层/每步 gate 值与 intervention delta / projection failure 的关系。

ICLR 最小可信组合不是只跑 A1/A2。若时间不足，至少需要：

1. A0 + A1 + A2 + A3/A4：证明 Tier-1 的实际作用与过耦合来源。
2. A5：证明 joint human 下降能否由 generated camera 条件解释。
3. A7 或 A8 的一个轻量真实训练 / smoke：证明方案不是只有采样期工具。若做不到，论文主张应降级为 reliability / diagnostic paper，而不是 structural disentanglement paper。

### 10.8 风险表

| 风险                                            | 严重程度 | 必须解决 / 可绕过 | 处理方案                                                                             | 对路线影响              |
| --------------------------------------------- | ---- | ---------- | -------------------------------------------------------------------------------- | ------------------ |
| 只分 text lane，latent 仍互相污染                     | 高    | 必须解决       | 不把 Module A 单独写成解耦；必须配 intervention、replay、oracle                                | 防止伪增量叙事            |
| camera projection 指标改善但 raw human dynamics 变差 | 高    | 必须解决       | 固定视角 human quality 是硬约束，projection 只能辅助评估                                        | 防止只优化构图            |
| branch-specific CFG 只是采样技巧                    | 中    | 必须解决       | 写成 PoseAnything-inspired diagnostic，不写成训练结构贡献                                    | 防止被审稿人质疑贡献弱        |
| two-stage boundary 对 checkpoint 敏感            | 中    | 可绕过        | 作为 P0 诊断，不作为唯一修复；扫描 0.3/0.5/0.7                                                  | 若不稳，转向 P1 gate     |
| residual gate 退化为恒开或恒关                        | 中    | 可绕过        | 与 fixed-open / fixed-closed 对照；若无增益就不保留                                          | gate 不能写成核心贡献      |
| MI / orthogonal 约束破坏生成质量                      | 高    | 可绕过        | 降级为 P2；只做 private 子空间诊断                                                          | 避免复杂高风险训练          |
| generated-camera replay 不能解释 joint human 下降   | 高    | 必须解决       | 继续查 text utilization、loss conflict、Stage2 generation error                       | 机制主张需要改写           |
| evaluator 与任务不匹配                              | 中    | 必须解决       | official metrics + fixed-view render + projection render + failure taxonomy 同时报告 | 避免只用 TMR/CLaTr 下结论 |

### 10.9 最小改动与后续大改

**可以马上做的最小改动**

1. P0 branch-specific CFG grid：不改训练，只改采样组合和 evaluation config。
2. P0 channel-gated CFG：直接用已有 `--channel-gated-cfg` 验证 human/camera guidance 是否应限制在各自 latent channels。
3. P0 full intervention matrix：把 human-text、camera-text、all-text 与 observed latent zero/shuffle/noise 补齐。
4. P0 generated-camera replay + GT-camera oracle：定位 joint human 下降来自 generated camera 条件质量还是 simultaneous denoising。
5. P0 projection render gate：只做 fixed-view + camera-projection 可视化与指标，不进入训练。

**后续大改**

1. P1 branch-specific condition adapter：需要训练轻量参数，作为 text lane 解耦。
2. P1 cross-branch residual gate：需要记录 gate trace 并做固定开/关消融。
3. P1 two-stage denoise schedule：若 P0 诊断显示 early contamination，再改 sampler 或 denoiser block。
4. P2 token-level masked attention：直接限制 human / camera token 可见性，但会重构 Stage2 主干。
5. P2 private-shared latent decomposition + MI / orthogonal regularization：只在 P0/P1 证明 latent 污染无法由轻量策略解决后考虑。

### 10.10 PoseAnything 问题的收紧解释

Figure 4 里看不到 camera 信息注入，不等于 PoseAnything 没有 camera control。Figure 4 是 pose-guided generation 主 pipeline：reference image、pose latent、PTCM 和 DiT 主干。相机控制主要在采样期的 decoupled CFG 里展示，也就是 Figure 5 / Figure 8 对应的 subject-camera control，而不是主 pipeline 中一个显式 camera encoder block。

PoseAnything 的 Eq.10：

$$
\tilde{\epsilon}=\hat{\epsilon}_{\theta}(\emptyset_s,z_c)+s\cdot(\hat{\epsilon}_{\theta}(z_s,\emptyset_c)-\hat{\epsilon}_{\theta}(\emptyset_s,z_c))
$$

可以理解为：以 camera-only prediction 作为基底，再加入 subject-only 相对 camera-only 的残差方向。直觉上，它让视频保留 camera motion anchor，同时把 subject pose following 拉回来。

但这个减法不是严格解耦证明。它依赖一个近似假设：subject condition 与 camera condition 在 denoising prediction 空间中可以被线性组合或残差分离。若两类条件高度耦合，这个公式可能只是经验上减少冲突，而不是保证 subject 与 camera 独立。

StoryMotion 借鉴时应做三点调整：

1. 使用 concat latent 的 channel mask，把 human guidance 和 camera guidance 写回各自 channels。
2. 保留 unconditional anchor，避免把 camera-only prediction 当成唯一基底。
3. 必须报告 swapping / intervention / replay：换 camera 时 human 是否保持，换 human 时 camera 是否保持。

### 10.11 对 InterGen-style 双向 latent 交互的收紧判断

用户提出的直观方案是：human 与 camera 解耦生成，各自使用自身 condition，并在每个 block 交互对方 latent，类似 InterGen 把 camera 当作另一个 human agent。当前判断是 **不推荐作为默认主路线**，但可以作为 fixed-open residual 的对照。

原因不是“不能交互”，而是 **不能无门槛、每层、双向交互**：

1. Human 与 camera 不是对称 agent。human branch 有骨架动力学、接触、语义动作等强约束；camera branch 更像观察器 / 构图控制器。把 camera 当另一个 human agent 会默认两者对称互相影响，这与当前 evidence 不符。
2. 已有 human completion 证据显示 observed camera latent 对 human branch 是强条件；joint mode 中 camera latent 是生成结果，一旦 generated camera 分布偏差，naive cross-block latent exchange 很可能把 camera error 放大为 human artifact。
3. InterGen-style 交互更适合多个同类实体的协调；StoryMotion 需要的是 **private branch + channel-gated guidance + intervention-validated residual gate**，而不是 full latent 全开放互读。

更稳的替代结构：

```text
human private path: z_h, c_h
camera private path: z_c, c_c
optional exchange: gated residual only when source branch confidence is high
post-check: fixed-view human quality + camera-projection render
```

P0 不应先训练大结构，而应先做四个诊断：

1. **generated-camera replay**：joint 生成 camera 后，固定该 camera 输入 human completion，比较 replay human 与 joint human。
2. **GT-camera oracle**：把 generated camera 替换为 GT camera，看 human 指标、fixed-view render 和 projection render 是否明显恢复。
3. **cross-branch perturbation**：shuffle / zero / noise-matched camera latent 对 human branch 的退化曲线。
4. **channel-gated CFG**：在不重训下检查分支 guidance 是否能降低互相污染。

### 10.12 写作边界

当前可以写：

> We diagnose human-camera over-coupling in a unified branch-mask latent diffusion model and introduce a bridge-free decoupling protocol: branch-specific and channel-gated guidance for sampling-time diagnosis, intervention and replay tests for causal attribution, and post-hoc camera-projection rendering as a reliability gate. Structural branch adapters and residual gates are evaluated only when the diagnostics show persistent cross-branch contamination.

当前不能写：

1. “StoryMotion 已经实现 human-camera 完全解耦。”
2. “MI / orthogonal 约束已证明有效。”
3. “branch-specific CFG 一定提升所有指标。”
4. “projection render 是生成机制的一部分。”
5. “gate 是最终贡献”，除非 fixed-open / fixed-closed / no-gate 消融证明 learned gate 必要。

### 10.13 2026-06-20 远端资源与并行任务分配

当前只读检查结论：

1. Codex 当前工具列表没有单独的 5090 MCP namespace；此前 `mcp__remote4090` 只暴露 2 张 RTX 4090。用户提醒后改用 `ssh 5090` 直连，确认 5090 主机可用。
2. `ssh 5090` 对应 host `user-SY8108G-D12R-G4`，`nvidia-smi -L` 显示 4 张 RTX 5090：GPU 0/1/2/3，均为空闲起步。
3. 5090 `/data` 可用，`df -h /data` 显示约 7.3T 总量、4.5T 可用。
4. `/datasets/pulp-redownloade` 当前不存在；因此没有发现该目录正在处理。如果之后该目录重新出现并有近期写入，应先等待处理结束，再启动正式实验。
5. 所有新输出只写 `/data`；不访问 `/data_broken`。

4 张 5090 已通过 SSH 确认可见，正式并行分配如下：

| GPU  | 任务                                                                     | 目标                                                            | 输出                                                                                                                                                                                  |
| ---- | ---------------------------------------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPU0 | branch-specific / channel-gated CFG official eval grid                 | 量化 PoseAnything-inspired sampling 是否降低 human-camera 条件冲突      | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_cfg_grid_20260620/`                                                                                                 |
| GPU1 | text + observed-latent intervention matrix                             | 区分 text lane 弱化、observed latent dominance、generated branch 污染 | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_intervention_20260620/`                                                                                             |
| GPU2 | fixed-view + camera-projection render gate，至少 100 samples              | 补齐 human motion 在 camera projection 下的可靠性可视化                  | `/data/public/ripemangobox/Motion/StoryMotion/stage2/vis/v4_projection_gate_20260620/` 与 `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_projection_gate_20260620/` |
| GPU3 | P1 adapter / residual-gate smoke 或 same-seed replay + GT-camera oracle | 若代码未完成 adapter/gate，则先做 replay/oracle 因果诊断，不训练新结构             | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_replay_oracle_20260620/`                                                                                            |

若只能使用 `mcp__remote4090` 而不能 SSH 5090，降级分配如下：

| GPU | 第一轮 | 第二轮 |
| --- | --- | --- |
| GPU0 | CFG official eval grid | projection render gate |
| GPU1 | intervention matrix | replay / GT-camera oracle |

不建议现在启动的任务：

1. Projection Consistency Bridge、projection loss、learned projection predictor。
2. 任何写入 `/data_broken` 的恢复或读取任务。
3. 在 `/datasets/pulp-redownloade` 重新出现且仍在写入时启动正式 eval/render/training。

2026-06-20T21:24+08:00 已在 5090 启动 4 个 tmux session：

| Session | GPU | 任务 | 输出 |
| --- | --- | --- | --- |
| `smv4_gpu0_cfg_20260620` | 0 | joint standard CFG 与 channel-gated CFG grid | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_cfg_grid_20260620/` |
| `smv4_gpu1_human_intervention_20260620` | 1 | human completion text / observed-camera latent intervention | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_human_intervention_20260620/` |
| `smv4_gpu2_projection_gate_20260620` | 2 | 100-sample fixed-view + camera-projection render gate | `/data/public/ripemangobox/Motion/StoryMotion/stage2/vis/v4_5090_projection_gate_source_20260620/` 与 `/data/public/ripemangobox/Motion/StoryMotion/stage2/vis/v4_5090_projection_gate_fair_compare_20260620/` |
| `smv4_gpu3_joint_text_intervention_20260620` | 3 | joint text intervention matrix | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_joint_text_intervention_20260620/` |

这些任务使用 independent-dropout checkpoint `runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt` 和 mixed full cache `runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110/val.pt`；没有启动 Projection Consistency Bridge、projection loss 或 learned projection predictor。

### 10.14 2026-06-21 human-camera 解耦诊断完成结果

2026-06-21T03:14+08:00，10.13 的 4 路 5090 任务全部完成；`/sys/fs/ext4/sdh1/errors_count=0`。汇总文件：

- `5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_analysis_20260621/completed_metrics.tsv`
- `5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_analysis_20260621/completed_deltas.tsv`
- `5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_analysis_20260621/projection_gate_motion_stats.tsv`

#### 10.14.1 Joint channel-gated CFG grid

Full mixed test，10549 samples。指标方向：rFPD、Out、FTD、CLaTr FCD 越低越好；TMR、CLaTr、F1 越高越好。

| setting                  | rFPD ↓ | Out ↓ |   FTD ↓ |  TMR ↑ | TMR cov ↑ | CLaTr FCD ↓ | CLaTr ↑ |  F1 ↑ |
| ------------------------ | -----: | ----: | ------: | -----: | --------: | ----------: | ------: | ----: |
| standard cfg2 eta1       |  0.505 | 0.075 | 155.920 | 24.036 |     0.373 |      85.991 |  33.416 | 0.380 |
| channel-gated h2/c2 eta0 |  0.632 | 0.088 | 152.020 | 22.767 |     0.365 |     100.052 |  27.861 | 0.306 |
| channel-gated h3/c1 eta0 |  0.777 | 0.097 | 154.769 | 23.679 |     0.341 |     102.338 |  19.374 | 0.235 |
| channel-gated h1/c3 eta0 |  0.694 | 0.094 | 166.325 | 17.928 |     0.385 |     105.971 |  34.324 | 0.360 |

结论边界：

1. 不能写 channel-gated CFG 优于 standard CFG。h2/c2 只在 FTD 上小幅改善，但 rFPD、Out、CLaTr FCD、CLaTr 与 F1 都明显变差。
2. 这支持一个较弱结论：当前 checkpoint 的 text-space bilateral/channel-gated sampler 不是直接可用的解耦改进，只能作为 diagnostic。
3. 后续若继续做 channel-gated，需要多 seed 或更小步长 grid；不能把单次 FTD 改善当作稳定收益。

#### 10.14.2 Joint text intervention

对比 standard cfg2 eta1。正数是否为好取决于指标方向；这里只记录差值。

| intervention | ΔrFPD ↓ | ΔOut ↓ | ΔFTD ↓ | ΔTMR ↑ | ΔCLaTr ↑ | ΔF1 ↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| zero camera text | +0.035 | +0.001 | +3.348 | +0.341 | -21.191 | -0.192 |
| shuffle camera text | +0.089 | +0.009 | -0.787 | -0.335 | -21.557 | -0.194 |
| zero human text | +0.277 | +0.002 | +32.671 | -19.763 | +8.887 | +0.076 |
| shuffle human text | +0.052 | +0.006 | -1.622 | -17.424 | -1.757 | -0.022 |

可写的诊断：

1. Human text 对 joint task 的 TMR-side human semantics 是强条件；zero / shuffle human text 使 TMR score 大幅下降。
2. Camera text 对 CLaTr / caption-side semantic alignment 是强条件；zero / shuffle camera text 使 CLaTr 与 F1 大幅下降。
3. Camera text 对当前几何指标影响较小；但这不能写成“camera text 对运动无影响”，因为 CLaTr / caption alignment 已明显退化，且缺少 camera-pose-specific metric。
4. zero human text 反而提高 CLaTr 与 F1 是反直觉结果，只能作为文本分支耦合/指标不完全对齐的警示，不能写成“human text 有害”。

#### 10.14.3 Human completion text / observed-camera latent intervention

Full mixed test，10549 samples；human completion 只报告 TMR-side human metrics。

| setting                        |    FTD ↓ |  TMR ↑ | coverage ↑ | precision ↑ | recall ↑ |      ΔFTD |    ΔTMR | Δcoverage |
| ------------------------------ | -------: | -----: | ---------: | ----------: | -------: | --------: | ------: | --------: |
| human base cfg2 eta1           |  126.590 | 18.181 |      0.846 |       0.805 |    0.930 |         — |       — |         — |
| zero camera text               |  126.099 | 18.267 |      0.848 |       0.805 |    0.931 |    -0.491 |  +0.086 |    +0.002 |
| shuffle camera text            |  126.452 | 18.187 |      0.845 |       0.805 |    0.930 |    -0.138 |  +0.006 |    -0.001 |
| observed camera latent zero    | 1913.848 |  9.844 |      0.001 |       0.069 |    0.449 | +1787.258 |  -8.337 |    -0.844 |
| observed camera latent shuffle |  192.535 |  5.043 |      0.570 |       0.649 |    0.699 |   +65.945 | -13.138 |    -0.276 |
| observed camera latent noise   | 1227.914 |  0.000 |      0.004 |       0.024 |    0.789 | +1101.324 | -18.181 |    -0.842 |

可写的诊断：

1. 在当前 human completion setting 下，camera text zero / shuffle 几乎不影响 TMR-side human metrics。
2. Observed camera latent 是强条件；zero / shuffle / noise-matched 会使 human completion 明显退化或崩溃。
3. 不能把这写成“模型忽略所有 text”或“camera latent 是唯一因果因素”。zero/noise latent 可能越出训练分布，shuffle latent 也改变了 sample-level pairing；因此这是依赖诊断，不是完整因果证明。

#### 10.14.4 100-sample projection / fair-compare render gate

输出：

- Source render：`5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/vis/v4_5090_projection_gate_source_20260620/`，1001 files，其中 700 MP4、300 PNG、1 JSON。
- Fair compare：`5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/vis/v4_5090_projection_gate_fair_compare_20260620/`，1202 files，其中 1000 MP4、100 PNG、102 JSON。

100-sample motion-stat aggregate：

| series                       |   n | MPJPE mean ↓ | contact absdiff mean ↓ | skate mean ↓ | joint vel mean | joint accel mean | root path mean |
| ---------------------------- | --: | -----------: | ---------------------: | -----------: | -------------: | ---------------: | -------------: |
| PulpMotion wz0/wc11          | 100 |       0.1739 |                 0.4083 |       0.0196 |         0.0183 |           0.0082 |         1.9718 |
| PulpMotion wz2/wc11          | 100 |       0.1588 |                 0.4051 |       0.0147 |         0.0115 |           0.0074 |         1.0942 |
| StoryMotion human completion | 100 |       0.0824 |                 0.2159 |       0.0271 |         0.0199 |           0.0078 |         2.1852 |
| StoryMotion joint            | 100 |       0.1785 |                 0.3769 |       0.0249 |         0.0187 |           0.0080 |         2.0126 |

解释边界：

1. Human completion 在这 100 个样本上 MPJPE 与 contact absdiff 明显优于 StoryMotion joint；这支持“给定 observed camera latent 时 human branch 更可靠”。
2. StoryMotion joint 的 MPJPE 接近或略差于 PulpMotion，contact absdiff 略好于 PulpMotion，但 skate 不占优；因此不能写成 joint human quality 已解决。
3. 该 render gate 是后验可靠性检查，不是生成机制本身。

#### 10.14.5 DeepSeek Max 反驳式复核摘要

DS Max 复核同意以下边界：

1. 不可写“channel-gated CFG 优于 standard CFG”。
2. 不可写“human-camera 已经解耦”。
3. 不可写“camera text 对视频运动无影响”；当前指标缺 camera-pose-specific metric，且 CLaTr / F1 明显受 camera text 影响。
4. 不可写“human text 有害”；zero human text 提升 CLaTr / F1 是反直觉现象，需要额外控制。
5. 当前实验是 dependency / intervention diagnostic，不是最终因果证明。

DS Max 建议下一批优先做 text-missing controls、cross-modal text replacement 与 oracle-latent intervention；在这些控制实验完成前，不应启动 P1 adapter / residual-gate 训练作为主线 claim。

### 10.15 2026-06-21 新一轮三卡 text-control 任务

基于 10.14，先不启动 P1 adapter / residual-gate 训练。原因：channel-gated CFG 尚未显示稳定收益，且文本分支贡献仍存在反直觉结果；直接训练新结构会把机制问题和训练收益混在一起。

新一轮 5090 三卡任务使用同一 checkpoint/cache：

- Checkpoint：`runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`
- Cache：`runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110/val.pt`

| Session | GPU | 任务 | 输出 | 判据 |
| --- | ---: | --- | --- | --- |
| `smv4_gpu0_joint_missing_text_20260621` | 0 | joint zero_all / shuffle_all text full eval | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_joint_missing_text_20260621/` | 若 all-text missing 同时损害 TMR 与 CLaTr，则说明 human/camera text halves 不是可独立解释的简单开关 |
| `smv4_gpu1_human_text_controls_20260621` | 1 | human completion zero/shuffle human text 与 zero/shuffle all text | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_human_text_controls_20260621/` | 判断 human completion 是否只对 observed camera latent 敏感，还是仍依赖 human text |
| `smv4_gpu3_camera_text_controls_20260621` | 3 | camera completion base 与 camera/human/all text controls | `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_camera_text_controls_20260621/` | 给 human completion 的结论做 camera-side 对称性检查 |

GPU2 暂时保留空闲。若这轮显示 camera completion 对 human text 或 all text 有强依赖，则下一步应写最小 cross-modal text replacement 脚本；若 text controls 全部稳定，再考虑 oracle-latent / generated-camera replay。 

### 10.16 2026-06-21 text-control 完成结果

2026-06-21T13:33+08:00 复核，10.15 的三卡任务已全部完成；5090 无残留 tmux，4 张 GPU 空闲，`/sys/fs/ext4/sdh1/errors_count=0`。新一轮共 13 个 full JSON 全部落盘：

- `v4_5090_joint_missing_text_20260621/`：2 个 JSON，records total = 21098。
- `v4_5090_human_text_controls_20260621/`：4 个 JSON，records total = 42196。
- `v4_5090_camera_text_controls_20260621/`：7 个 JSON，records total = 73843。

汇总文件：

- `5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_analysis_20260621/text_controls_metrics_20260621.tsv`
- `5090:/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v4_5090_analysis_20260621/text_controls_deltas_20260621.tsv`

#### 10.16.1 Joint all-text missing control

Full mixed test，10549 samples。对比 baseline 为 `joint_std_cfg2_eta1`。指标方向：rFPD、Out、FTD、CLaTr FCD 越低越好；TMR、CLaTr、F1 越高越好。

| setting             | rFPD ↓ | Out ↓ |   FTD ↓ |  TMR ↑ | coverage ↑ | CLaTr FCD ↓ | CLaTr ↑ |  F1 ↑ |    ΔTMR |  ΔCLaTr |    ΔF1 |
| ------------------- | -----: | ----: | ------: | -----: | ---------: | ----------: | ------: | ----: | ------: | ------: | -----: |
| joint std cfg2 eta1 |  0.505 | 0.075 | 155.920 | 24.036 |      0.373 |      85.991 |  33.416 | 0.380 |   0.000 |   0.000 |  0.000 |
| zero camera text    |  0.540 | 0.076 | 159.268 | 24.377 |      0.350 |      83.331 |  12.225 | 0.188 |  +0.341 | -21.191 | -0.192 |
| zero human text     |  0.782 | 0.077 | 188.591 |  4.272 |      0.355 |      89.194 |  42.304 | 0.456 | -19.763 |  +8.887 | +0.076 |
| zero all text       |  0.531 | 0.050 | 229.120 |  5.116 |      0.316 |      97.091 |  10.897 | 0.177 | -18.920 | -22.519 | -0.203 |
| shuffle camera text |  0.594 | 0.085 | 155.134 | 23.701 |      0.374 |      95.028 |  11.860 | 0.186 |  -0.335 | -21.556 | -0.194 |
| shuffle human text  |  0.557 | 0.081 | 154.299 |  6.612 |      0.372 |      91.213 |  31.660 | 0.358 | -17.424 |  -1.757 | -0.022 |
| shuffle all text    |  0.658 | 0.089 | 154.008 |  6.408 |      0.369 |      97.419 |  10.885 | 0.175 | -17.628 | -22.532 | -0.205 |

诊断更新：

1. `zero_all` 与 `shuffle_all` 同时打掉 TMR、CLaTr 与 caption F1，说明 joint task 不能被解释成“human text 只管 TMR，camera text 只管 CLaTr”的简单独立开关；两半文本在统一 joint sampling 中存在指标层面的耦合。
2. `zero_all` 的 rFPD 和 Out 反而更低，不能被写成质量提升；它同时带来 FTD、TMR、CLaTr FCD、CLaTr 与 F1 的明显退化，更像文本缺失后生成变保守或指标错位。
3. 10.14 中 `zero_human_text` 提升 CLaTr / F1 的反直觉现象没有被 all-text 控制支持为可用改进；all-text zero / shuffle 都会显著损害 CLaTr 与 F1。
4. 当前仍缺 camera-pose-specific metric，因此不能写“文本只影响语义、不影响相机轨迹”。

#### 10.16.2 Human completion text controls

Full mixed test，10549 samples；human completion 只报告 TMR-side human metrics。对比 baseline 为 `human_base_cfg2_eta1`。

| setting | FTD ↓ | TMR ↑ | coverage ↑ | precision ↑ | recall ↑ | ΔFTD | ΔTMR | Δcoverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| human base cfg2 eta1 | 126.590 | 18.181 | 0.846 | 0.805 | 0.930 | 0.000 | 0.000 | 0.000 |
| zero camera text | 126.099 | 18.267 | 0.848 | 0.805 | 0.931 | -0.491 | +0.086 | +0.002 |
| shuffle camera text | 126.452 | 18.187 | 0.845 | 0.805 | 0.930 | -0.138 | +0.006 | -0.001 |
| zero human text | 126.225 | 18.129 | 0.847 | 0.806 | 0.931 | -0.365 | -0.052 | +0.002 |
| shuffle human text | 127.560 | 17.850 | 0.842 | 0.801 | 0.927 | +0.970 | -0.331 | -0.004 |
| zero all text | 126.068 | 18.127 | 0.845 | 0.803 | 0.932 | -0.521 | -0.054 | -0.001 |
| shuffle all text | 127.542 | 17.852 | 0.842 | 0.801 | 0.927 | +0.952 | -0.329 | -0.004 |
| observed camera latent zero | 1913.848 | 9.844 | 0.001 | 0.069 | 0.449 | +1787.258 | -8.337 | -0.844 |
| observed camera latent shuffle | 192.535 | 5.043 | 0.570 | 0.649 | 0.699 | +65.945 | -13.138 | -0.276 |
| observed camera latent noise | 1227.914 | 0.000 | 0.004 | 0.024 | 0.789 | +1101.324 | -18.181 | -0.842 |

诊断更新：

1. Human completion 对 text zero / shuffle 的敏感性仍很弱：human text 和 all text 的 zero 基本不伤 TMR-side metrics，shuffle human / all text 只有小幅退化。
2. 这与 observed camera latent intervention 的巨大退化形成强对比；当前 human completion 更像主要依赖 observed camera latent 与 motion prior，而不是强依赖文本语义。
3. 不能据此写“文本无用”。现有指标只覆盖 TMR-side human distribution，不覆盖 fine-grained action correctness、caption alignment 或 per-sample semantic faithfulness。
4. 后续若要证明 text lane 是否被忽略，需要做 per-sample text replacement / action-category stratification，而不是只看 aggregate TMR。

#### 10.16.3 Camera completion text controls

Camera completion 的 JSON 没有 proj rFPD / outscreen 指标；本节只报告 CLaTr 与 caption metrics。对比 baseline 为 `camera_base_cfg2_eta1`。

| setting | CLaTr FCD ↓ | CLaTr ↑ | coverage ↑ | caption F1 ↑ | precision ↑ | recall ↑ | ΔCLaTr | ΔF1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| camera base cfg2 eta1 | 14.495 | 54.847 | 0.870 | 0.638 | 0.664 | 0.628 | 0.000 | 0.000 |
| zero camera text | 14.679 | 52.236 | 0.872 | 0.608 | 0.635 | 0.598 | -2.611 | -0.030 |
| shuffle camera text | 15.355 | 52.093 | 0.864 | 0.604 | 0.631 | 0.593 | -2.754 | -0.035 |
| zero human text | 15.253 | 56.417 | 0.864 | 0.653 | 0.680 | 0.642 | +1.570 | +0.015 |
| shuffle human text | 14.910 | 54.471 | 0.864 | 0.633 | 0.659 | 0.622 | -0.376 | -0.005 |
| zero all text | 16.262 | 53.466 | 0.854 | 0.620 | 0.653 | 0.612 | -1.381 | -0.019 |
| shuffle all text | 16.076 | 51.698 | 0.859 | 0.601 | 0.627 | 0.589 | -3.148 | -0.038 |

诊断更新：

1. Camera completion 对 camera text 有中等敏感性：zero / shuffle camera text 均降低 CLaTr 与 caption F1。
2. all-text missing 也降低 camera-side semantic metrics，尤其 `shuffle_all` 的 CLaTr 与 F1 退化最大。
3. human text 对 camera completion 没有稳定负效应；`zero_human_text` 反而提升 CLaTr / F1，`shuffle_human_text` 接近 baseline。这更像 text-branch coupling 或指标不完全对齐，不能写成“删除 human text 改善 camera completion”。
4. 因为缺少 camera trajectory / framing-specific 指标，本节不能证明 camera motion 本身是否受 text intervention 影响。

#### 10.16.4 当前路线判断

更新后的结论：

1. `channel-gated CFG` 仍只能作为 diagnostic，不能作为主贡献写“优于 standard CFG”。
2. Human completion 的 aggregate TMR-side metrics 对 text perturbation 很稳，但对 observed camera latent 极敏感；这支持“observed camera latent 是当前 human completion 的强条件”，不支持“human-camera 已经解耦”。
3. Joint task 的 all-text controls 证明文本通道不是简单可分离开关；human text、camera text 与 all text 的退化模式互相不对称。
4. Camera completion 对 camera/all text 有语义退化，但缺 camera-specific metric；下一步必须补 camera trajectory / framing metric 或 per-sample replacement，而不是继续只堆 CLaTr / caption。

下一步优先级：

1. 写最小 cross-modal text replacement eval：swap human text only、swap camera text only、swap all text，并按 task 类型分别报告 aggregate 与 per-sample delta。
2. 补 camera-specific metric：camera trajectory distance、framing / outscreen、projection gate 中的 subject-in-frame stability。
3. 做 generated-camera replay / GT-camera oracle：把 joint generated camera 输入 human completion，并用 GT camera 替换做 oracle upper bound。
4. 在上述诊断完成前，继续暂缓 P1 adapter / residual-gate 训练；否则训练收益会和条件依赖机制混在一起。
