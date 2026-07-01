---
hypothesis: "StoryMotion V5 的有效证据集中在 Pulp Stage1 主路线；source tokenizer 加入 latent Z-score 后仍出现 Stage2 官方指标坍塌，projection containment loss 虽显著改善画面包含度，但会进一步损害动作与相机语义。"
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
updated: 2026-06-24T20:55:21+08:00
supersedes: "[[2026-06-16_storymotion-v3-formal]]"
---

# StoryMotion V5：官方指标证据版

> [!abstract] 核心结论
> StoryMotion V5 的可写正向证据只来自 Pulp Stage1 主路线：frozen Pulp tokenizer + Stage2 branch-mask latent diffusion 可以统一支持 joint generation、human completion 和 camera completion。主路线在 mixed / pure joint generation 上显著改善 geometry、outscreen、human distribution coverage 和 camera coverage；camera 语义指标不是全面最优。Completion 可作为应用候选，但缺少 single-task completion baseline，暂不支持公平胜出结论。Source VAE / HFSQ / GRFSQ Stage1 加入 train-set latent Z-score 后，8 组同口径 Stage2 official human metrics 仍整体坍塌；缺失 Z-score 不是充分解释，geo loss、joint / separate tokenizer 和 with-z / no-z 选择也未恢复有效生成。Source-tokenizer projection containment loss 能把 joint Out 从 `24.92%` 降到 `5.18%` 或 `1.49%`，但会进一步损害 human 与 camera official metrics。Pulp 主路线上的 `w=0.01` joint-only screen containment 已定位为 eval 聚合代码 bug：旧 run 在 `step=148000` 首次 eval 前未保存 checkpoint，不能从 `148000` 原地续跑；修复后从 `step=146000` 重新启动完整 rerun，已通过旧崩溃点 `148000` 的首次 eval 并保存 checkpoint，但完整官方评估仍未完成，当前仍不能作为 V5 性能证据。
>
> | 证据项 | 关键指标 | 数值 / 状态 |
> | ------ | -------- | ----------- |
> | Pulp 主路线 mixed joint | FDframing / Out / FDTMR / Human Cov / Camera Cov | `0.535` / `7.89%` / `155.73` / `36.43%` / `62.83%` |
> | Pulp 主路线 pure joint | FDframing / Out / FDTMR / Human Cov / Camera Cov | `0.414` / `5.98%` / `137.30` / `46.06%` / `61.39%` |
> | source tokenizer Z-score 失败区间 | FDTMR / Human Cov | `1308.67–1413.23` / `0.049%–0.691%` |
> | source projection `w=0.01` | Out / FDTMR / Camera Cov | `5.18%` / `1332.05` / `38.81%` |
> | source projection `w=0.05` | Out / FDTMR / Camera Cov | `1.49%` / `1356.19` / `36.47%` |
> | Pulp screen containment evalfix | resume / target / verification | `146000 -> 196000`；`step=148000` 首次 eval 已通过，eval loss `0.01393`，Out `0.04127`，`last.pt` / `best_eval.pt` 已保存 |

## 1. 评估口径

Stage2 使用 PulpMotion latent contract：

```text
z = concat([z_hum, z_cam]) in R^{192 x T}
z_hum in R^{128 x T}
z_cam in R^{64 x T}
```

三种任务共享同一 branch-mask diffusion checkpoint，只改变 observed branch 与 target branch：

| 模式                | 条件                   | 生成分支           | 当前用途                        |
| ----------------- | -------------------- | -------------- | --------------------------- |
| joint generation  | text                 | human + camera | 主性能证据                       |
| human completion  | text + camera latent | human latent   | 应用候选；需 single-task baseline |
| camera completion | text + human latent  | camera latent  | 应用候选；需 single-task baseline |

表中的 `Stage2 ratio` 表示模型在 camera completion、human completion、joint generation 三种任务上的训练配比。`with_z` 表示 camera feature 为 `xyz + rot6d`；`no_z` 表示删除 camera translation depth，仅保留 `xy + rot6d`。

证据优先级：

| 等级                             | 可写结论             | 当前用途                                                             |
| ------------------------------ | ---------------- | ---------------------------------------------------------------- |
| official full metrics          | 可以写性能结论          | FDTMR、TMR、R3、Human Cov、FDCLaTr、CLaTr、F1、Camera Cov、FDframing、Out |
| Stage1 official reconstruction | 可以写 tokenizer 上界 | GT identity / Pulp Stage1 reconstruction                         |
| feature / latent loss only     | 不写性能结论           | 只用于训练监控或后续实验排程                                                   |

## 2. 主路线结果

### 2.1 Joint Generation

测试目标：验证 Pulp Stage1 latent contract 下，单个 branch-mask Stage2 是否能在 text-only joint generation 中优于 PulpMotion baseline。

Mixed full test：

| model                           | split | Stage2 ratio | FDframing ↓ |  Out ↓ | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ |
| ------------------------------- | ----- | ------------ | ----------: | -----: | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: |
| PulpMotion DiT `(x,y)` Aux      | mixed | -            |       3.777 | 17.35% |  428.53 | 24.97 | 12.42% |       8.55% |     82.19 |   33.28 | 36.67% |       48.09% |
| PulpMotion MAR `(x,y)` Aux      | mixed | -            |       6.399 | 36.18% |  296.96 | 23.53 | 17.06% |      16.15% |    113.97 |   41.94 | 42.23% |       55.10% |
| StoryMotion independent-dropout | mixed | `1:1:1`      |       0.535 |  7.89% |  155.73 | 23.95 | 26.05% |      36.43% |     85.70 |   33.52 | 37.40% |       62.83% |

Pure full test：

| model                           | split | Stage2 ratio | FDframing ↓ |  Out ↓ | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ |
| ------------------------------- | ----- | ------------ | ----------: | -----: | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: |
| PulpMotion DiT `(x,y)` Aux      | pure  | -            |       5.893 | 28.47% |  414.80 | 21.66 | 10.54% |      13.82% |     93.27 |   37.78 | 51.27% |       44.81% |
| PulpMotion MAR `(x,y)` Aux      | pure  | -            |       5.079 | 25.15% |  276.80 | 21.55 | 16.01% |      25.88% |     99.26 |   53.55 | 67.74% |       53.59% |
| PulpMotion MAR `(x,y,z)` Aux    | pure  | -            |       5.139 | 27.38% |  258.54 | 20.48 | 17.05% |      26.65% |    113.30 |   51.19 | 63.72% |       55.39% |
| StoryMotion independent-dropout | pure  | `1:1:1`      |       0.414 |  5.98% |  137.30 | 21.42 | 25.73% |      46.06% |     92.80 |   44.73 | 59.90% |       61.39% |

结论：StoryMotion 主路线在 mixed / pure 上稳定改善 geometry、outscreen、FDTMR、Human Cov 和 Camera Cov。Camera semantic alignment 不是全面最优；pure split 的 CLaTr / F1 仍低于 PulpMotion MAR。

### 2.2 Completion

测试目标：验证同一个 Stage2 checkpoint 是否能在给定一支 GT latent 时补全另一支 latent，用于应用候选判断。

| split | mode              | Stage2 ratio | task                   | samples | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ |
| ----- | ----------------- | ------------ | ---------------------- | ------: | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: |
| mixed | camera completion | `1:1:1`      | text + human -> camera |   10549 |       - |     - |      - |           - |     14.50 |   54.85 | 63.76% |       87.15% |
| mixed | human completion  | `1:1:1`      | text + camera -> human |   10549 |  126.71 | 18.17 | 21.83% |      84.61% |         - |       - |      - |            - |
| pure  | camera completion | `1:1:1`      | text + human -> camera |    4053 |       - |     - |      - |           - |     32.05 |   55.33 | 72.82% |       82.19% |
| pure  | human completion  | `1:1:1`      | text + camera -> human |    4053 |  110.70 | 16.27 | 20.80% |      90.03% |         - |       - |      - |            - |

结论：completion 任务指标表现有潜力，但当前缺少同 tokenizer、同 backbone、同 split 的 single-task completion 对照，因此本研究不宣称在 completion 任务上实现公平优胜。

### 2.3 Stage1 上界

测试目标：确认 Pulp Stage1 tokenizer 本身不是瓶颈，并给 Stage2 generation 设置可达到的 reconstruction upper bound。

| split | mode                       | FDTMR ↓ | Human Cov ↑ | FDCLaTr ↓ | Camera Cov ↑ | FDframing ↓ | Out ↓ |
| ----- | -------------------------- | ------: | ----------: | --------: | -----------: | ----------: | ----: |
| mixed | GT identity                |      ~0 |     100.00% |        ~0 |      100.00% |      0.0020 | 0.89% |
| mixed | Pulp Stage1 reconstruction |  124.48 |      85.34% |     15.52 |       87.15% |       0.238 | 4.64% |
| pure  | GT identity                |      ~0 |     100.00% |        ~0 |       99.95% |      0.0025 | 0.71% |
| pure  | Pulp Stage1 reconstruction |  109.34 |      92.43% |     17.66 |       84.68% |       0.137 | 3.47% |

结论：Stage1 reconstruction 明显优于 Stage2 generation，说明主瓶颈仍在 Stage2 生成、采样或条件利用，而不是评估器本身。

## 3. Task Ratio 结果

测试目标：验证三任务训练配比从 `1:1:1` 调到 `1:1:2` 是否能改善 joint generation，尤其是 camera-side 指标。

| split | ratio   | FDframing ↓ |  Out ↓ | FDTMR ↓ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ |
| ----- | ------- | ----------: | -----: | ------: | ----------: | --------: | ------: | -----: | -----------: |
| mixed | `1:1:1` |       0.782 | 10.17% |  157.29 |      34.38% |     84.30 |   30.87 | 35.04% |       63.70% |
| mixed | `1:1:2` |       0.807 |  9.79% |  154.21 |      36.25% |     83.16 |   35.23 | 38.34% |       64.89% |
| pure  | `1:1:1` |       0.504 |  7.48% |  135.81 |      44.63% |     99.59 |   41.39 | 56.63% |       58.94% |
| pure  | `1:1:2` |       0.530 |  6.99% |  134.83 |      45.69% |     85.56 |   46.29 | 60.68% |       62.42% |

结论：`1:1:2` 对 joint / camera-side 更稳，尤其改善 camera semantic metrics 与 coverage；但它没有解决 completion 缺公平 baseline 的问题，也不构成 human-camera 解耦证明。

## 4. Source Tokenizer 诊断

### 4.1 Stage2 Latent Z-score

测试目标：判断 train-set per-channel latent Z-score 能否修复 source tokenizer 接入 Stage2 后的模式坍塌。

公平口径为 pure full-test human completion：4053 个样本、相同 Stage2 task ratio `1:1:2`、50-step sampling、CFG `2.0`、eta `1.0`，并统一评估最后一个训练 checkpoint。选择 human completion 是因为它是 8 组配置都不需要额外 depth-z 协议的共同 official task；no-z camera / joint 不纳入该表。

| Stage1 / tokenizer  | camera | geo loss | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | MPJPE ↓ | Contact Δ ↓ |
| ------------------- | ------ | -------- | ------: | ----: | -----: | ----------: | ------: | ----------: |
| Pulp Stage1 主路线（参考） | with-z | -        |  112.28 | 15.86 | 20.92% |     90.576% |  0.0860 |      0.1741 |
| joint VAE           | with-z | no-geo   | 1323.83 |  9.43 |  9.82% |      0.568% |  0.1825 |      0.5220 |
| joint VAE           | with-z | `w=0.1`  | 1308.67 |  9.17 |  9.67% |      0.568% |  0.1846 |      0.5234 |
| joint HFSQ          | no-z   | no-geo   | 1413.23 | 10.38 |  9.72% |      0.173% |  0.2030 |      0.5321 |
| joint HFSQ          | no-z   | `w=0.1`  | 1349.48 | 10.23 | 10.09% |      0.049% |  0.2070 |      0.5306 |
| separate VAE        | no-z   | no-geo   | 1340.97 | 10.04 | 10.51% |      0.370% |  0.2074 |      0.5266 |
| separate VAE        | no-z   | `w=0.1`  | 1315.21 | 10.09 | 10.54% |      0.691% |  0.2084 |      0.5292 |
| separate GRFSQ      | no-z   | no-geo   | 1376.84 | 10.67 | 10.71% |      0.271% |  0.2050 |      0.5293 |
| separate GRFSQ      | no-z   | `w=0.1`  | 1314.39 | 10.35 | 11.13% |      0.370% |  0.2081 |      0.5256 |

结论：

1. **Z-score 没有修复坍塌**：8 组 source tokenizer 的 FDTMR 仍为 `1308.67–1413.23`，Human Coverage 仅为 `0.049%–0.691%`；Pulp 主路线参考值为 `112.28` 和 `90.576%`。
2. **geo loss 只产生坍塌区间内的局部波动**：部分配置的 FDTMR 改善，但 TMR、R3、MPJPE 和 coverage 没有一致收益，不能视为恢复有效生成。
3. **结构选择不是单一主因**：joint / separate、VAE / HFSQ / GRFSQ、with-z / no-z 均出现同类失效。Z-score 是合理的分布预处理，但仅对齐一阶、二阶统计不足以对齐 decoder 可用流形。

### 4.2 Projection Containment Loss

测试目标：验证基于 GT 可见关节的可微相机投影包含度约束，能否降低 joint generation 的出屏率，并判断其对动作与相机语义的副作用。

公平口径为同一 with-z joint VAE、同一 train-set latent Z-score、同一 pure split、相同 Stage2 task ratio `1:1:2`、4053 个样本、50-step sampling、CFG `2.0`、eta `1.0` 和最后一个训练 checkpoint。唯一训练变量是 projection containment loss 权重；official eval 使用完整测试集。

Joint generation：

| projection loss | FDframing ↓ |  Out ↓ | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | MPJPE ↓ |
| --------------- | ----------: | -----: | ------: | ----: | -----: | ----------: | ------: |
| disabled        |       5.159 | 24.92% | 1188.89 |  6.87 | 10.17% |      0.370% |  0.2114 |
| `w=0.01`        |       1.724 |  5.18% | 1332.05 |  3.74 |  9.45% |      0.148% |  0.2496 |
| `w=0.05`        |       2.141 |  1.49% | 1356.19 |  2.32 |  8.44% |      0.222% |  0.2541 |

| projection loss | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ |
| --------------- | --------: | ------: | -----: | -----------: |
| disabled        |    201.31 |   30.31 | 41.07% |       42.96% |
| `w=0.01`        |    229.49 |   26.86 | 35.64% |       38.81% |
| `w=0.05`        |    238.81 |   23.50 | 29.85% |       36.47% |
|                 |           |         |        |              |

Completion：

| task | projection loss | distribution distance ↓ | semantic score ↑ | R3 / F1 ↑ | coverage ↑ | MPJPE ↓ |
| ---- | --------------- | ----------------------: | ---------------: | ---------: | ---------: | ------: |
| human | disabled | FDTMR 1323.83 | TMR 9.43 | R3 9.82% | 0.568% | 0.1825 |
| human | `w=0.01` | FDTMR 1394.43 | TMR 5.70 | R3 9.20% | 0.346% | 0.2382 |
| human | `w=0.05` | FDTMR 1547.42 | TMR 2.91 | R3 7.30% | 0.395% | 0.2549 |
| camera | disabled | FDCLaTr 193.03 | CLaTr 40.24 | F1 47.18% | 55.14% | - |
| camera | `w=0.01` | FDCLaTr 230.90 | CLaTr 35.69 | F1 42.26% | 47.60% | - |
| camera | `w=0.05` | FDCLaTr 258.71 | CLaTr 30.92 | F1 33.95% | 40.86% | - |

结论：

1. **包含度目标有效**：`w=0.01` 将 FDframing 降低 `66.6%`、Out 降低 `79.2%`；`w=0.05` 将 Out 降低 `94.0%`。该 loss 确实能驱动画面内约束，而不是无效正则项。
2. **当前优化存在明显目标冲突**：几何收益伴随 joint human、joint camera、human completion 和 camera completion 的一致退化。更高权重只进一步压低 Out，没有形成更好的整体 Pareto 点。
3. **`w=0.01` 优于 `w=0.05`，但仍不可作为正式模型**：除 Out 外，`w=0.01` 在几何、动作和相机指标上整体更好；但它仍显著弱于无 projection-loss 基线的语义指标，并且没有修复 source tokenizer 坍塌。
4. **正确定位是辅助约束，不是主损失**：后续只应在稳定的 Pulp 主路线上测试，并限制其梯度作用范围，避免通过收缩动作幅度或牺牲语义多样性获得低出屏率。

## 5. Loss-only 结果处理

1. Stage1 feature reconstruction loss、Stage2 latent loss 和 decoded feature loss 均不等价于 official generation quality，不进入性能证据表。
2. 第 4 节的判断只基于同 split、同 task、同采样设置的 full official metrics。
3. 后续实验必须先通过 official metric gate；不再用更低的训练 loss 或单独的 geo loss 变化推断生成质量改善。

## 6. Controlled Coupling 诊断

5090 上的 `stage2/metrics/v5_controlled_coupling_20260624/` 已完成 mixed full test `10549` samples 的 dependency matrix（A `15/15`）、generated-camera replay（B）、GT-camera oracle（C）和 two-stage boundary schedule（D）。这批结果用于定位 Stage2 branch-mask 主路线的依赖结构，不作为新性能模型。

直白结论：

1. **Completion 两个方向在当前设置下没有测出对 text noise 的明显依赖**。Camera completion 的 text noise camera / human / all 分别为 FDCLaTr `15.16 / 15.20 / 15.66`、F1 `62.45% / 62.43% / 61.71%`、Camera Cov `86.50% / 86.71% / 86.75%`。Human completion 的 text noise camera / human / all 分别为 FDTMR `126.70 / 126.66 / 126.77`、Human Cov 均为 `84.61%`、MPJPE `0.0884 / 0.0888 / 0.0888`。
2. **Observed branch 是 completion 的主导变量**。Camera completion 中破坏 observed human branch 后退化明显：additive noise 为 FDCLaTr `303.00`、F1 `27.82%`、Camera Cov `31.04%`；zero 后 FDCLaTr `1044.19`、F1 `3.79%`、Camera Cov `0.35%`。Human completion 中 observed camera additive noise 使 FDTMR 到 `154.70`、Human Cov 到 `72.91%`、MPJPE 到 `0.1162`。
3. **Joint mode 对 text perturbation 敏感**。Joint shared-noise baseline 为 FDTMR `153.72`、TMR `23.91`、R3 `26.38%`、Human Cov `36.77%`、FDCLaTr `84.82`、F1 `37.81%`、Out `7.72%`、MPJPE `0.1928`。Text noise all 后 TMR 到 `18.26`、F1 到 `27.08%`；text shuffle all 后 TMR 到 `6.37`、F1 到 `17.70%`；text zero all 后 FDTMR 到 `228.16`、TMR 到 `4.79`、R3 到 `5.66%`。
4. **B/C/D 是定位，不是修复**。Generated-camera replay 与 joint baseline 同区间，不能解释或修复 joint human 退化。GT-camera oracle 给出几何/覆盖上界（Human Cov `84.58%`、MPJPE `0.0884`），但 TMR `18.17` 低于 joint / replay 的 `23+`，说明强 camera 条件会压制文本语义。Boundary `0.3 -> 0.7` 让 Human Cov `59.38% -> 77.96%`、MPJPE `0.1354 -> 0.1073`，但 TMR `19.82 -> 18.83` 下降；它是 coupling strength tradeoff，不是 Pareto 修复。

因此，V5 主线当前不是“修复已经完成”，而是“问题已定位”：completion 有 hard observed-branch dominance，joint 有 text sensitivity 和 branch pollution 风险。下一步机制应是 soft observed branch、learned coupling gate 和 relation-space projection constraint，而不是继续把三模式统一本身当作主要 claim。

## 7. 坍塌原因判断

“缺失 latent Z-score”已被否定为充分解释。当前更符合证据的判断是：source tokenizer 与 Stage2 之间存在高阶 latent contract 或 decoder-manifold 不匹配。Z-score 只校正逐通道均值和方差，不能保证 sampled latent 保留时序相关性、跨分支语义结构或落在 decoder 的有效区域。

具体风险：

1. **Stage1 上界未知**：source Stage1 尚未完成 direct encode-decode official reconstruction，无法排除 tokenizer 本身已丢失 official metric 所需信息。
2. **采样分布偏离**：即使真实 source latent 可解码，Stage2 sampled latent 也可能离开训练流形；需要 teacher-forced decode 与 sampled decode 的 official gap 定位。
3. **离散流形不匹配**：HFSQ / GRFSQ decoder 依赖量化码流形，而连续 diffusion 输出未显式投影回合法码域。
4. **语义 contract 不等价**：维度、顺序和边际统计对齐不代表 source latent 具备 Pulp latent 的条件语义、跨分支关系和 decoder 鲁棒性。

当前结论是 source VAE / HFSQ / GRFSQ 不能作为 Pulp Stage1 的 drop-in replacement。现有证据足以停止继续做单纯 Z-score、geo weight 或 loss-only sweep，但仍不足以把根因唯一归到 Stage1 或 Stage2。

## 8. 限制

1. 8 组公平比较仅覆盖 human completion；no-z camera / joint 仍需定义 depth-z 回填或预测协议。
2. source Stage1 direct official reconstruction 尚未完成，Stage1 上界未知。
3. 当前结果来自单次训练和单 checkpoint 评估，尚无多 seed 方差。
4. Completion 主路线仍缺少同 tokenizer、同 backbone、同 split 的 single-task baseline。
5. Projection containment loss 当前只有 source with-z joint VAE 完成 official full eval；Pulp 主路线的旧 `w=0.01` joint-only run 在 `step=148000` eval 聚合阶段崩溃，未保存 `last.pt` / `best_eval.pt`，不能从该步原地续跑。eval 聚合已修复，新 rerun 已通过 `step=148000` 首次 eval 并保存 checkpoint，但在完整 official eval 完成前仍不能作为 Pulp 主路线性能结论。
6. Source tokenizer 不生成 intrinsics；projection 实验使用 GT intrinsics passthrough，因此不是完整相机内参生成评估。

## 9. 下一步

### tokenizer
1. 补 source Stage1 direct encode-decode official reconstruction，先判断 VAE / HFSQ / GRFSQ tokenizer 是否具备可用上界。
2. 对同一批 source Stage2 runs 做 teacher-forced latent decode 与 sampled latent decode 的 official 对照，定位偏差是在 tokenizer 还是生成分布。
3. 若 Stage1 上界通过，再做最小 latent-manifold 适配：Pulp-latent distillation、可学习 affine adapter 或显式 manifold regularization；HFSQ / GRFSQ 需加入量化感知投影。
### 明确不做
1. 所有后续路线以 full official metrics 为继续条件，不再扩展 loss-only 或 geo-weight sweep。

### Projection containment
1. 以 `independent_dropout_ft_20260614`（Pulp Stage1 frozen tokenizer 主线）为起点，添加 `w=0.01` screen projection loss 训练。仅对 joint generation task 反传 containment 梯度，保持 completion 分支不受影响。与不加 loss 的 indepdrop baseline 做同口径 pure full-test 对比，以 Out + human/camera semantic non-regression 为继续条件。若未形成 Pareto 改善则停止该路线。
2. 2026-06-24 4090 失败 run：旧 run dir 为 `runs/train/stage2/v5_indepdrop_screen_projection_20260624/gpu0_indepdrop_screen_w0p01_jointonly_sub16_b512`，日志为 `logs/indepdrop_screen_w0p01_joint_only_gpu0_20260624.log`。配置确认正确：从 `independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt` 的 `step=146000` 续训，目标 `196000`，`w=0.01`、`pulp_autoencoder` decoder、每 batch 最多 16 个 projection samples，`screen_projection_task_scope = joint`。
3. 旧 run 实际只写到 `step=148000`，没有 `last.pt` / `best_eval.pt`。训练日志均值仅可作为监控：`screen_projection_loss = 0.0472`，weighted loss `0.000472`，train-time `screen_projection_outscreen = 0.0386`，generated visible fraction `0.6614`，GT visible fraction `0.5205`。首次 eval 聚合时报错：`numpy.core._exceptions._UFuncNoLoopError`，原因是 `evaluate()` 对包含字符串字段 `screen_projection_task_scope = joint` 的 metric list 执行 `np.mean`。根因是代码级指标聚合 bug，不是 GPU / 设备问题，也不是 screen containment 架构本身失效。
4. 修复状态：`evaluate()` 已改为只聚合有限数值字段，并在 eval / test 前先保存 `last.pt`，避免后续评估失败再次丢失当前训练步。`runs/train/stage2/_check_indepdrop_screen_w0p01_evalfix_20260624` 已从 `step=146000` 跑到 `146001`，写出 `train` / `eval` / `test` 三类记录，并产生 `last.pt` 与 `best_eval.pt`。
5. 续跑状态：不能从旧 run 的 `step=148000` 原地续跑，因为没有 checkpoint；已从可用的 `step=146000` checkpoint 启动新 run `runs/train/stage2/v5_indepdrop_screen_projection_20260624/gpu0_indepdrop_screen_w0p01_jointonly_sub16_b512_evalfix`，日志为 `logs/indepdrop_screen_w0p01_joint_only_gpu0_evalfix_20260624.log`，目标仍为 `196000`。该 rerun 已通过旧崩溃点 `step=148000` 的首次 eval：eval loss `0.013931`，`joint_screen_projection_loss = 0.030371`，`joint_screen_projection_outscreen = 0.041274`，并已保存 `last.pt` / `best_eval.pt`。后续仍需完整 official eval 才能判断 projection containment 是否在 Pulp 主路线形成 Pareto 改善。
